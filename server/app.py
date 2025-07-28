# app.py
# 2025-01-28 16:55:00
# Updated to use hybrid storage system with user management

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
import time
import re
import json
import uuid
from utils.hybrid_storage import storage_manager
from utils.user_manager import user_manager

# Import API modules
from api.quarterly_stats import register_quarterly_stats_routes

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process-file', methods=['POST'])
def process_file():
    """
    Hybrid storage file processing - stores in memory and database
    """
    
    start_time = time.time()
    
    try:
        # Parse request body
        body = request.get_json()
        
        filename = body.get('filename', 'unknown.csv')
        file_content = body.get('content', '')
        chart_config = body.get('chart_config', {})
        session_id = body.get('session_id')  # Get session ID from request
        
        # Get or create user ID
        user_id = user_manager.get_or_create_user_id(session_id)
        
        # Store file using hybrid approach
        file_id = storage_manager.store_file(user_id, file_content, filename)
        
        # Get the processed DataFrame
        df = storage_manager.get_file_df(user_id, file_id)
        
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
            'filename': filename,
            'file_id': file_id,
            'user_id': user_id
        }
        
        response = {
            'data': data_json,
            'chart_elements': chart_elements,
            'processing_info': processing_info,
            'columns': columns,
            'file_id': file_id,
            'session_id': session_id or str(uuid.uuid4())
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to process file'
        }), 500

@app.route('/format-chart', methods=['POST'])
def format_chart():
    """
    Format chart endpoint - same functionality as process-file for now
    """
    return process_file()

@app.route('/api/files', methods=['GET'])
def get_user_files():
    """Get list of files for the current user"""
    try:
        session_id = request.args.get('session_id')
        user_id = user_manager.get_or_create_user_id(session_id)
        
        files = storage_manager.get_user_files(user_id)
        
        return jsonify({
            'files': files,
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to get user files'
        }), 500

@app.route('/api/files/<file_id>', methods=['GET'])
def get_file_data(file_id):
    """Get file data for charting"""
    try:
        session_id = request.args.get('session_id')
        user_id = user_manager.get_or_create_user_id(session_id)
        
        df = storage_manager.get_file_df(user_id, file_id)
        
        if df is None:
            return jsonify({
                'error': 'File not found'
            }), 404
        
        # Clean and standardize the data
        cleaned_df = clean_and_standardize_data(df)
        
        # Auto-detect columns for chart
        columns = list(cleaned_df.columns)
        x_column = columns[0] if len(columns) > 0 else None
        y_column = columns[1] if len(columns) > 1 else None
        
        # Generate smart chart elements
        chart_elements = format_chart_elements(cleaned_df, x_column, y_column, 'bar')
        
        # Convert to JSON-serializable format
        data_json = cleaned_df.to_dict('records')
        
        response = {
            'data': data_json,
            'chart_elements': chart_elements,
            'columns': columns,
            'file_id': file_id
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to get file data'
        }), 500

@app.route('/api/files/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete a file"""
    try:
        session_id = request.args.get('session_id')
        user_id = user_manager.get_or_create_user_id(session_id)
        
        storage_manager.delete_file(user_id, file_id)
        
        return jsonify({
            'message': 'File deleted successfully',
            'file_id': file_id
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to delete file'
        }), 500

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

# Register API routes
register_quarterly_stats_routes(app)

if __name__ == '__main__':
    print("🚀 Starting GetCharty Local Server...")
    print("📊 Server will be available at: http://localhost:5000")
    print("🌐 Client will be available at: http://localhost:8000")
    print("📁 Upload your CSV files to see the magic!")
    app.run(debug=True, host='0.0.0.0', port=5000) 