import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self, data_path='data/test_data.csv'):
        self.data_path = data_path
        self.df = None
        
        # Define Thresholds (Absolute limits for "Reasoning")
        # Normal: Safe range
        # Warning: Gray area (User defined)
        # Critical: User defined "Abnormal"
        self.rules = {
            'temp': {
                'normal_min': 45, 'normal_max': 50,
                'critical_high': 52, 'critical_low': 43
                # Implied: 50 < x <= 52 is Warning High, 43 <= x < 45 is Warning Low
            },
            'pressure': {
                'normal_min': 1.00, 'normal_max': 1.05,
                'critical_high': 1.08, 'critical_low': 0.97
            },
            'vibration': {
                'normal_min': 0.02, 'normal_max': 0.04,
                'critical_high': 0.07
                # Warning Low: < 0.02 (User requested)
            }
        }
        
        # Verification weights for composite score (relative importance)
        self.weights = {'temp': 1.0, 'pressure': 2.0, 'vibration': 3.0} # Example: Vibration is critical

    def load_data(self):
        """Loads data and converts timestamp."""
        try:
            self.df = pd.read_csv(self.data_path)
            
            # 1. Missing Value Handling (Forward Fill for Time Series)
            if self.df.isnull().sum().sum() > 0:
                print(f"[Warning] Found missing values. Filling with ffill.")
                self.df.fillna(method='ffill', inplace=True)
                self.df.fillna(method='bfill', inplace=True) # Fallback for first row

            # 2. Basic Data Validation (Physical constraints)
            # Temp > 0, Pressure > 0, Vibration >= 0
            original_len = len(self.df)
            self.df = self.df[
                (self.df['temp'] > 0) & 
                (self.df['pressure'] > 0) & 
                (self.df['vibration'] >= 0)
            ]
            
            if len(self.df) < original_len:
                print(f"[Info] Removed {original_len - len(self.df)} invalid records.")

            if 'timestamp' in self.df.columns:
                self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            print(f"Loaded {len(self.df)} records.")
        except FileNotFoundError:
            print(f"Error: File {self.data_path} not found.")
            self.df = pd.DataFrame()

    def calculate_statistical_scores(self):
        """
        Calculates Z-scores for the dataset.
        Using these statistical measures for robust scoring.
        """
        features = ['temp', 'pressure', 'vibration']
        if self.df.empty:
            return

        X = self.df[features].values
        
        # 1. Z-Scores
        self.scaler = StandardScaler().fit(X)
        X_z = self.scaler.transform(X)
        self.df[['z_temp', 'z_pressure', 'z_vibration']] = X_z
        
        # 2. Composite Rule Score (Weighted Z-Score sum of absolute deviations)
        # We use absolute Z-score because deviation in either direction is interesting.
        # This provides a continuous "baseline" scan.
        weighted_z = np.abs(X_z) * np.array([self.weights[f] for f in features])
        self.df['rule_score'] = weighted_z.sum(axis=1)

    def _check_threshold(self, value, metric_name):
        """Helper to check thresholds for a given metric."""
        rules = self.rules[metric_name]
        reasons = []
        is_issue = False
        
        # Check High Limits
        if 'critical_high' in rules and value > rules['critical_high']:
            is_issue = True
            reasons.append(f"CRITICAL: {metric_name.capitalize()} High ({value} > {rules['critical_high']})")
        elif 'normal_max' in rules and value > rules['normal_max']:
            is_issue = True
            reasons.append(f"WARNING: {metric_name.capitalize()} High ({value} > {rules['normal_max']})")
            
        # Check Low Limits (Skip for Vibration as low is good)
        if metric_name != 'vibration':
            if 'critical_low' in rules and value < rules['critical_low']:
                is_issue = True
                reasons.append(f"CRITICAL: {metric_name.capitalize()} Low ({value} < {rules['critical_low']})")
            elif 'normal_min' in rules and value < rules['normal_min']:
                is_issue = True
                reasons.append(f"WARNING: {metric_name.capitalize()} Low ({value} < {rules['normal_min']})")
                
        return is_issue, reasons

    def detect_anomalies(self):
        """
        Detects anomalies using a hybrid approach:
        1. Hard Rule Violations (Domain Knowledge)
        2. Statistical Scoring (Z-score)
        
        Returns a list of anomalies with enriched info.
        """
        if self.df is None or self.df.empty:
            return []

        # Ensure statistical scores are present
        self.calculate_statistical_scores()

        anomalies = []

        for index, row in self.df.iterrows():
            row_is_issue = False
            row_reasons = []
            features = ['temp', 'pressure', 'vibration']
            
            # --- Check 1: Hard Rules (Domain) using Helper ---
            for feature in features:
                is_issue, reasons = self._check_threshold(row[feature], feature)
                if is_issue:
                    row_is_issue = True
                    row_reasons.extend(reasons)
            
            if row_is_issue:
                # Construct the anomaly record
                # We use the calculated statistical scores for the 'severity' metric
                anomalies.append({
                    'index': index,
                    'timestamp': row['timestamp'],
                    'data': {k: row[k] for k in features},
                    'reasons': row_reasons,
                    'score': round(row['rule_score'], 2) # Weighted Z-score sum
                })
        
        return anomalies

if __name__ == "__main__":
    detector = AnomalyDetector()
    detector.load_data()
    
    anomalies = detector.detect_anomalies()
    print(f"\nFound {len(anomalies)} anomalies (Hybrid).")
    
    # Sort by Score desc
    anomalies.sort(key=lambda x: x['score'], reverse=True)
    
    for a in anomalies[:5]:
        print(f"[{a['timestamp']}] Score: {a['score']} | {'; '.join(a['reasons'])}")
