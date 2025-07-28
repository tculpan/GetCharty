# utils/data_processor.py
# 2025-01-28 16:55:00
# Updated to work with DataFrames and hybrid storage

import pandas as pd

def process_uploaded_file(df, date_columns=None):
    """Process DataFrame to add quarter and year information"""
    # Add quarter information
    for col in date_columns or []:
        if col in df.columns:
            df[f'{col}_quarter'] = pd.to_datetime(df[col]).dt.quarter
            df[f'{col}_year'] = pd.to_datetime(df[col]).dt.year
    
    return df