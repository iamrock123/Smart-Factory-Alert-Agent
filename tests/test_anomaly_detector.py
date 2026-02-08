import pytest
import pandas as pd
from anomaly_detector import AnomalyDetector

@pytest.fixture
def detector():
    return AnomalyDetector(data_path='data/test_data.csv')

class TestAnomalyDetector:
    def test_initialization(self, detector):
        assert detector.data_path == 'data/test_data.csv'
        assert detector.df is None
        assert 'temp' in detector.rules
        assert 'pressure' in detector.rules
        assert 'vibration' in detector.rules

    @pytest.mark.parametrize("metric, value, expected_issue, expected_reason_part", [
        # Temp Rules: Normal 45-50
        ("temp", 47.0, False, None),
        ("temp", 51.0, True, "WARNING: Temp High"),
        ("temp", 53.0, True, "CRITICAL: Temp High"),
        ("temp", 44.0, True, "WARNING: Temp Low"),
        ("temp", 42.0, True, "CRITICAL: Temp Low"),
        
        # Pressure Rules: Normal 1.00-1.05
        ("pressure", 1.02, False, None),
        ("pressure", 1.07, True, "WARNING: Pressure High"),
        ("pressure", 1.09, True, "CRITICAL: Pressure High"),
        ("pressure", 0.98, True, "WARNING: Pressure Low"),
        ("pressure", 0.95, True, "CRITICAL: Pressure Low"),

        # Vibration Rules: Normal 0.02-0.04 (Low is good)
        ("vibration", 0.03, False, None),
        ("vibration", 0.01, False, None), # Better than normal
        ("vibration", 0.06, True, "WARNING: Vibration High"),
        ("vibration", 0.08, True, "CRITICAL: Vibration High"),
    ])
    def test_check_threshold(self, detector, metric, value, expected_issue, expected_reason_part):
        is_issue, reasons = detector._check_threshold(value, metric)
        assert is_issue == expected_issue
        if expected_issue:
            assert len(reasons) > 0
            assert expected_reason_part in reasons[0]
        else:
            assert len(reasons) == 0

    def test_detect_anomalies_workflow(self, detector):
        # Create a mock dataframe
        data = {
            'timestamp': ['2024-01-01 10:00:00', '2024-01-01 10:05:00'],
            'temp': [47.0, 55.0],        # Normal, Critical High
            'pressure': [1.02, 1.02],    # Normal, Normal
            'vibration': [0.03, 0.03]    # Normal, Normal
        }
        detector.df = pd.DataFrame(data)
        detector.df['timestamp'] = pd.to_datetime(detector.df['timestamp'])
        
        anomalies = detector.detect_anomalies()
        
        assert len(anomalies) == 1
        assert anomalies[0]['index'] == 1
        assert "CRITICAL: Temp High" in anomalies[0]['reasons'][0]
        assert 'rule_score' in detector.df.columns
