import pytest
import pandas as pd
from data_generator import generate_sensor_data

def test_generate_sensor_data_structure():
    rows = 20
    df = generate_sensor_data(num_rows=rows)
    
    assert len(df) == rows
    assert list(df.columns) == ['timestamp', 'temp', 'pressure', 'vibration']
    # Check that it's a string-like column (could be object or string dtype)
    assert pd.api.types.is_string_dtype(df['timestamp'])

def test_generate_sensor_data_ranges():
    # Generate enough data to likely cover normal ranges
    df = generate_sensor_data(num_rows=100)
    
    # Check if values are generally within physically possible bounds (sanity check)
    assert df['temp'].min() > 0
    assert df['temp'].max() < 100
    assert df['pressure'].min() > 0
    assert df['pressure'].max() < 2.0
    assert df['vibration'].min() >= 0
    assert df['vibration'].max() < 1.0

def test_no_future_data():
    df = generate_sensor_data(num_rows=5)
    assert pd.to_datetime(df['timestamp']) is not None
