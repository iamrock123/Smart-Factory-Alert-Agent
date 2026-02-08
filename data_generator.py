import pandas as pd
import numpy as np
import random
import argparse
from datetime import datetime, timedelta

def generate_sensor_data(num_rows=100, start_date=None):
    """
    Generates dummy sensor data with timestamp, temp, pressure, vibration.
    Injects ~10% anomalies based on user-defined ranges.
    """
    
    # Define ranges
    # temp: normal 45–50, abnormal >52 or <43
    # pressure: normal 1.00–1.05, abnormal >1.08 or <0.97
    # vibration: normal 0.02–0.04, abnormal >0.07

    data = []
    if start_date:
         current_time = datetime.strptime(start_date, '%Y-%m-%d')
    else:
         # Default to 2024-06-03 00:00:00 as requested
         current_time = datetime(2024, 6, 3, 0, 0, 0)
    
    for _ in range(num_rows):
        is_anomaly = random.random() < 0.10  # 10% chance of anomaly/warning
        
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        if not is_anomaly:
            # Generate normal data
            temp = round(random.uniform(45, 50), 2)
            pressure = round(random.uniform(1.00, 1.05), 3)
            vibration = round(random.uniform(0.02, 0.04), 4)
            label = 'normal'
        else:
            # Generate abnormal/warning data
            # 50% chance of Critical, 50% chance of Warning
            severity = random.choice(['critical', 'warning'])
            anomaly_type = random.choice(['temp', 'pressure', 'vibration', 'mixed'])
            
            # Defaults
            temp = round(random.uniform(45, 50), 2)
            pressure = round(random.uniform(1.00, 1.05), 3)
            vibration = round(random.uniform(0.02, 0.04), 4)

            # Temp
            if anomaly_type in ['temp', 'mixed']:
                if random.choice([True, False]): # High
                    if severity == 'critical': temp = round(random.uniform(52.1, 60), 2)
                    else: temp = round(random.uniform(50.1, 52.0), 2) # Warning High
                else: # Low
                    if severity == 'critical': temp = round(random.uniform(30, 42.9), 2)
                    else: temp = round(random.uniform(43.0, 44.9), 2) # Warning Low
            
            # Pressure
            if anomaly_type in ['pressure', 'mixed']:
                if random.choice([True, False]): # High
                    if severity == 'critical': pressure = round(random.uniform(1.081, 1.20), 3)
                    else: pressure = round(random.uniform(1.051, 1.08), 3) # Warning High
                else: # Low
                    if severity == 'critical': pressure = round(random.uniform(0.80, 0.969), 3)
                    else: pressure = round(random.uniform(0.97, 0.999), 3) # Warning Low

            # Vibration
            if anomaly_type in ['vibration', 'mixed']:
                 if random.choice([True, False]): # High
                    if severity == 'critical': vibration = round(random.uniform(0.071, 0.15), 4)
                    else: vibration = round(random.uniform(0.041, 0.07), 4) # Warning High
                 else: # Low
                    vibration = round(random.uniform(0.00, 0.019), 4) # Warning Low (Always warning)
            
            label = f'abnormal_{severity}'
        
        data.append({
            'timestamp': timestamp,
            'temp': temp,
            'pressure': pressure,
            'vibration': vibration,
        })
        
        current_time += timedelta(minutes=5)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate dummy sensor data for Anomaly Alert Agent.')
    parser.add_argument('--rows', type=int, default=10, help='Number of rows to generate (default: 100)')
    args = parser.parse_args()

    print(f"Generating {args.rows} rows of sensor data...")
    df = generate_sensor_data(num_rows=args.rows)
    output_file = "data/test_data.csv"
    df.to_csv(output_file, index=False)
    print(f"Data generated and saved to {output_file}")
    print(df.head())
