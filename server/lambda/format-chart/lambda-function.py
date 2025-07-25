#server/lambda/process-file/lambda_function.py
import json
import pandas as pd
import io
import time
import re

def lambda_handler(event, context):
    """
    Simple server-side file processing for ChartDomain
    Demonstrates smart formatting and text processing
    """
    
    start_time = time.time()
    
    try:
        # Parse request body
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']
        
        filename = body.get('filename', 'unknown.csv')
        file_content = body.get('content', '')
        chart_config = body.get('chart_config', {})
        
        # Process CSV to DataFrame
        df = pd.read_csv(io.StringIO(file_content))
        
        # Clean and standardize the data
        cleaned_df = clean_and_standardize_data(df)
        
        # Auto-detect columns for chart
        columns = list(cleaned_df.columns)
        x_column = columns[0] if len(columns) > 0 else None
        y_column = columns[1] if len(columns) > 1 else None
        
        # Generate smart chart elements
        chart_elements = format_chart_elements(cleaned_df, x_column, y_column, chart_config.get('chart_type', 'bar'))
        
        # Convert to JSON-serializable format
        data_json = cleaned_df.to_dict('records')
        
        # Processing info
        processing_info = {
            'duration': round((time.time() - start_time) * 1000, 2),
            'rows_processed': len(cleaned_df),
            'columns_processed': len(cleaned_df.columns),
            'filename': filename
        }
        
        response = {
            'data': data_json,
            'chart_elements': chart_elements,
            'processing_info': processing_info,
            'columns': columns
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to process file'
            })
        }

def clean_and_standardize_data(df):
    """
    Clean and standardize data for professional presentation
    """
    cleaned_df = df.copy()
    
    # Clean column names
    cleaned_df.columns = [clean_column_name(col) for col in df.columns]
    
    # Remove completely empty rows
    cleaned_df = cleaned_df.dropna(how='all')
    
    # Clean each column based on its type
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            # Clean text columns
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            cleaned_df[col] = cleaned_df[col].replace('nan', '')
        elif cleaned_df[col].dtype in ['float64', 'int64']:
            # Clean numeric columns
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
    
    return cleaned_df

def clean_column_name(name):
    """
    Convert raw column names to clean, standardized format
    """
    # Remove special characters and standardize
    cleaned = re.sub(r'[^\w\s]', '', str(name))
    cleaned = re.sub(r'\s+', '_', cleaned.strip())
    return cleaned.lower()

def format_chart_elements(df, x_column, y_column, chart_type):
    """
    Generate professional chart titles and labels
    This is the proprietary server-side formatting
    """
    
    # Smart title generation
    title = generate_smart_title(x_column, y_column, chart_type)
    
    # Professional axis labels
    x_label = format_axis_label(x_column, df[x_column] if x_column else None)
    y_label = format_axis_label(y_column, df[y_column] if y_column else None)
    
    return {
        'title': title,
        'x_label': x_label,
        'y_label': y_label
    }

def generate_smart_title(x_col, y_col, chart_type):
    """
    Generate intelligent chart titles based on data context
    """
    if not x_col or not y_col:
        return "Data Visualization"
    
    # Format column names for display
    x_display = format_column_name_for_display(x_col)
    y_display = format_column_name_for_display(y_col)
    
    # Generate context-aware titles
    if chart_type == 'bar':
        return f"{y_display} by {x_display}"
    elif chart_type == 'line':
        return f"{y_display} Trends"
    elif chart_type == 'pie':
        return f"Distribution of {x_display}"
    elif chart_type == 'scatter':
        return f"{y_display} vs {x_display}"
    else:
        return f"{y_display} by {x_display}"

def format_column_name_for_display(column_name):
    """
    Convert technical column names to professional display names
    """
    if not column_name:
        return "Data"
    
    # Replace underscores with spaces and title case
    formatted = column_name.replace('_', ' ').replace('-', ' ')
    
    # Handle common abbreviations
    replacements = {
        'qty': 'Quantity',
        'amt': 'Amount',
        'rev': 'Revenue', 
        'cust': 'Customer',
        'prod': 'Product',
        'cat': 'Category',
        'pct': 'Percentage',
        'yr': 'Year',
        'mo': 'Month',
        'dt': 'Date',
        'num': 'Number',
        'val': 'Value',
        'id': 'ID'
    }
    
    words = formatted.split()
    for i, word in enumerate(words):
        word_lower = word.lower()
        if word_lower in replacements:
            words[i] = replacements[word_lower]
        else:
            words[i] = word.capitalize()
    
    return ' '.join(words)

def format_axis_label(column_name, data_series):
    """
    Create professional axis labels with units and context
    """
    base_label = format_column_name_for_display(column_name)
    
    if data_series is None or len(data_series) == 0:
        return base_label
    
    # Sample some values for analysis
    sample_values = data_series.dropna().head(20)
    
    if len(sample_values) == 0:
        return base_label
    
    # Currency detection
    if detect_currency(sample_values):
        return f"{base_label} (USD)"
    
    # Percentage detection
    elif detect_percentage(sample_values):
        return f"{base_label} (%)"
    
    # Large number formatting
    elif detect_large_numbers(sample_values):
        max_val = float(sample_values.max())
        if max_val > 1000000:
            return f"{base_label} (Millions)"
        elif max_val > 1000:
            return f"{base_label} (Thousands)"
    
    return base_label

def detect_currency(series):
    """Detect if values represent currency"""
    # Check if any string values contain currency symbols
    string_values = series.astype(str)
    return any('$' in str(val) or 'usd' in str(val).lower() for val in string_values)

def detect_percentage(series):
    """Detect if values represent percentages"""
    try:
        numeric_series = pd.to_numeric(series, errors='coerce').dropna()
        if len(numeric_series) == 0:
            return False
        
        # Check if values are in typical percentage range
        return (numeric_series >= 0).all() and (numeric_series <= 100).all() and numeric_series.max() > 1
    except:
        return False

def detect_large_numbers(series):
    """Detect if values are large numbers that should be scaled"""
    try:
        numeric_series = pd.to_numeric(series, errors='coerce').dropna()
        if len(numeric_series) == 0:
            return False
        
        return numeric_series.max() > 1000
    except:
        return False