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
from datetime import datetime, timedelta
from utils.hybrid_storage import storage_manager
from utils.user_manager import user_manager

# Import API modules
from api.quarterly_stats import register_quarterly_stats_routes

# Month names for consistent formatting
MONTH_NAMES = {
    1: 'Jan', 2: 'Feb', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

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

@app.route('/api/auto-spacing', methods=['POST'])
def auto_spacing():
    """
    Auto-spacing endpoint for X-axis labels
    """
    try:
        data = request.get_json()
        x_labels = data.get('x_labels', [])
        chart_type = data.get('chart_type', 'vertical_bar')
        
        if not x_labels:
            return jsonify({
                'success': False,
                'error': 'No X-axis labels provided'
            }), 400
        
        # Detect time interval and apply appropriate spacing
        interval_type = detect_time_interval(x_labels)
        
        if interval_type:
            xaxis_config = apply_time_spacing(x_labels, interval_type)
        else:
            xaxis_config = apply_default_spacing(x_labels)
        
        return jsonify({
            'success': True,
            'xaxis_config': xaxis_config,
            'interval_type': interval_type
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def detect_time_interval(x_labels):
    """
    Detect if labels represent time series and determine interval
    """
    try:
        # Try to parse dates from labels
        dates = []
        for label in x_labels[:10]:  # Sample first 10 labels
            # Skip if label is "Date" or similar header
            if str(label).lower() in ['date', 'time', 'period', '']:
                continue
                
            try:
                # Try various date formats
                for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', 
                           '%m/%d/%Y %H:%M', '%Y-%m-%d %H:%M', '%H:%M', '%Y-%m',
                           '%d-%b-%y', '%d-%b-%Y', '%Y/%m/%d', '%d/%m/%Y',
                           '%b %d, %Y', '%B %d, %Y', '%d %b %Y', '%d %B %Y']:
                    try:
                        date = datetime.strptime(str(label), fmt)
                        dates.append(date)
                        break
                    except ValueError:
                        continue
            except:
                continue
        
        if len(dates) < 3:
            return None  # Not enough valid dates
        
        # Calculate time differences
        intervals = []
        for i in range(1, len(dates)):
            diff = dates[i] - dates[i-1]
            intervals.append(diff)
        
        if not intervals:
            return None
        
        # Determine interval type
        avg_interval = sum(intervals, timedelta(0)) / len(intervals)
        
        if avg_interval <= timedelta(hours=2):
            return 'hour'
        elif avg_interval <= timedelta(days=2):
            return 'day'
        elif avg_interval <= timedelta(weeks=2):
            return 'week'
        elif avg_interval <= timedelta(days=45):
            return 'month'
        elif avg_interval <= timedelta(days=120):
            return 'quarter'
        elif avg_interval >= timedelta(days=300):
            return 'year'
        else:
            return 'other'
            
    except Exception as e:
        print(f"Error detecting time interval: {e}")
        return None

def apply_time_spacing(x_labels, interval_type):
    """
    Apply appropriate spacing based on time interval type
    """
    try:
        dates = []
        for label in x_labels:
            # Skip if label is "Date" or similar header
            if str(label).lower() in ['date', 'time', 'period', '']:
                dates.append(None)
                continue
                
            try:
                for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', 
                           '%m/%d/%Y %H:%M', '%Y-%m-%d %H:%M', '%H:%M', '%Y-%m',
                           '%d-%b-%y', '%d-%b-%Y', '%Y/%m/%d', '%d/%m/%Y',
                           '%b %d, %Y', '%B %d, %Y', '%d %b %Y', '%d %B %Y']:
                    try:
                        date = datetime.strptime(str(label), fmt)
                        dates.append(date)
                        break
                    except ValueError:
                        continue
            except:
                dates.append(None)
        
        if interval_type == 'hour':
            return apply_hourly_spacing(dates, x_labels)
        elif interval_type == 'day':
            return apply_daily_spacing(dates, x_labels)
        elif interval_type == 'week':
            return apply_weekly_spacing(dates, x_labels)
        elif interval_type == 'month':
            return apply_monthly_spacing(dates, x_labels)
        elif interval_type == 'quarter':
            return apply_quarterly_spacing(dates, x_labels)
        elif interval_type == 'year':
            return apply_yearly_spacing(dates, x_labels)
        else:
            return apply_default_spacing(x_labels)
            
    except Exception as e:
        print(f"Error applying time spacing: {e}")
        return apply_default_spacing(x_labels)

def apply_hourly_spacing(dates, x_labels):
    """Show every 6th hour: 0600, 1200, 1800, 2400"""
    tickvals = []
    ticktext = []
    
    for i, (date, label) in enumerate(zip(dates, x_labels)):
        if date and date.hour in [0, 6, 12, 18]:
            tickvals.append(i)
            ticktext.append(date.strftime('%H:%M'))
    
    # Check if the final label follows the same spacing pattern as other labels
    if len(tickvals) > 2:
        # Calculate the typical spacing between labels
        spacings = []
        for i in range(1, len(tickvals)):
            spacing = tickvals[i] - tickvals[i-1]
            spacings.append(spacing)
        
        if spacings:
            # Calculate average spacing (excluding the last interval)
            avg_spacing = sum(spacings[:-1]) / len(spacings[:-1]) if len(spacings) > 1 else spacings[0]
            
            # Check if the final spacing is significantly different from average
            final_spacing = spacings[-1] if spacings else 0
            if abs(final_spacing - avg_spacing) > avg_spacing * 0.5:  # If more than 50% different
                # Remove the final label as it doesn't follow the pattern
                tickvals.pop()
                ticktext.pop()
    
    return {
        'tickmode': 'array',
        'tickvals': tickvals,
        'ticktext': ticktext,
        'tickangle': 0,
        'showticklabels': True,
        'showgrid': False,
        'ticks': 'outside',
        'ticklen': 8,
        'tickwidth': 2,
        'tickcolor': 'black',
        'showline': True,
        'linecolor': 'black',
        'linewidth': 1
    }

def apply_daily_spacing(dates, x_labels):
    """Show only Mondays"""
    tickvals = []
    ticktext = []
    
    for i, (date, label) in enumerate(zip(dates, x_labels)):
        if date and date.weekday() == 0:  # Monday
            tickvals.append(i)
            ticktext.append(date.strftime('%a %m/%d'))
    
    # Check if the final label follows the same spacing pattern as other labels
    if len(tickvals) > 2:
        # Calculate the typical spacing between labels
        spacings = []
        for i in range(1, len(tickvals)):
            spacing = tickvals[i] - tickvals[i-1]
            spacings.append(spacing)
        
        if spacings:
            # Calculate average spacing (excluding the last interval)
            avg_spacing = sum(spacings[:-1]) / len(spacings[:-1]) if len(spacings) > 1 else spacings[0]
            
            # Check if the final spacing is significantly different from average
            final_spacing = spacings[-1] if spacings else 0
            if abs(final_spacing - avg_spacing) > avg_spacing * 0.5:  # If more than 50% different
                # Remove the final label as it doesn't follow the pattern
                tickvals.pop()
                ticktext.pop()
    
    return {
        'tickmode': 'array',
        'tickvals': tickvals,
        'ticktext': ticktext,
        'tickangle': 0,
        'showticklabels': True,
        'showgrid': False,
        'ticks': 'outside',
        'ticklen': 8,
        'tickwidth': 2,
        'tickcolor': 'black',
        'showline': True,
        'linecolor': 'black',
        'linewidth': 1
    }

def apply_weekly_spacing(dates, x_labels):
    """Show every 4th week, starting with 4th week"""
    tickvals = []
    ticktext = []
    
    for i, (date, label) in enumerate(zip(dates, x_labels)):
        if date and i >= 3 and (i - 3) % 4 == 0:  # Start from 4th week, every 4th
            tickvals.append(i)
            ticktext.append(date.strftime('%d %B %Y'))
    
    # Check if the final label follows the same spacing pattern as other labels
    if len(tickvals) > 2:
        # Calculate the typical spacing between labels
        spacings = []
        for i in range(1, len(tickvals)):
            spacing = tickvals[i] - tickvals[i-1]
            spacings.append(spacing)
        
        if spacings:
            # Calculate average spacing (excluding the last interval)
            avg_spacing = sum(spacings[:-1]) / len(spacings[:-1]) if len(spacings) > 1 else spacings[0]
            
            # Check if the final spacing is significantly different from average
            final_spacing = spacings[-1] if spacings else 0
            if abs(final_spacing - avg_spacing) > avg_spacing * 0.5:  # If more than 50% different
                # Remove the final label as it doesn't follow the pattern
                tickvals.pop()
                ticktext.pop()
    
    return {
        'tickmode': 'array',
        'tickvals': tickvals,
        'ticktext': ticktext,
        'tickangle': 0,
        'showticklabels': True,
        'showgrid': False,
        'ticks': 'outside',
        'ticklen': 8,
        'tickwidth': 2,
        'tickcolor': 'black',
        'showline': True,
        'linecolor': 'black',
        'linewidth': 1
    }

def apply_monthly_spacing(dates, x_labels):
    """Show every 3rd month: March, June, Sept, Dec"""
    tickvals = []
    ticktext = []
    
    for i, (date, label) in enumerate(zip(dates, x_labels)):
        if date and date.month in [3, 6, 9, 12]:
            tickvals.append(i)
            ticktext.append(f"{MONTH_NAMES[date.month]} {date.year}")
    
    # Check if the final label follows the same spacing pattern as other labels
    if len(tickvals) > 2:
        # Calculate the typical spacing between labels
        spacings = []
        for i in range(1, len(tickvals)):
            spacing = tickvals[i] - tickvals[i-1]
            spacings.append(spacing)
        
        if spacings:
            # Calculate average spacing (excluding the last interval)
            avg_spacing = sum(spacings[:-1]) / len(spacings[:-1]) if len(spacings) > 1 else spacings[0]
            
            # Check if the final spacing is significantly different from average
            final_spacing = spacings[-1] if spacings else 0
            if abs(final_spacing - avg_spacing) > avg_spacing * 0.5:  # If more than 50% different
                # Remove the final label as it doesn't follow the pattern
                tickvals.pop()
                ticktext.pop()
    
    return {
        'tickmode': 'array',
        'tickvals': tickvals,
        'ticktext': ticktext,
        'tickangle': 0,
        'showticklabels': True,
        'showgrid': False,
        'ticks': 'outside',
        'ticklen': 8,
        'tickwidth': 2,
        'tickcolor': 'black',
        'showline': True,
        'linecolor': 'black',
        'linewidth': 1
    }

def apply_quarterly_spacing(dates, x_labels):
    """Show final quarter of each year"""
    tickvals = []
    ticktext = []
    
    # Filter out None dates
    valid_dates = [(i, date) for i, date in enumerate(dates) if date]
    
    if len(valid_dates) < 2:
        return apply_default_spacing(x_labels)
    
    # Group dates by year and find the final quarter of each year
    year_groups = {}
    for idx, date in valid_dates:
        year = date.year
        if year not in year_groups:
            year_groups[year] = []
        year_groups[year].append((idx, date))
    
    # For each year, find the latest quarter (highest month)
    labeled_indices = set()
    for year in sorted(year_groups.keys()):
        year_dates = year_groups[year]
        # Find the date with the highest month in this year
        latest_date = max(year_dates, key=lambda x: x[1].month)
        idx, date = latest_date
        tickvals.append(idx)
        ticktext.append(f"{MONTH_NAMES[date.month]} {date.year}")
        labeled_indices.add(idx)
    
    # Drop the final label if it's not the final quarter of the year
    if tickvals and len(tickvals) > 1:
        last_idx = tickvals[-1]
        last_date = None
        for idx, date in valid_dates:
            if idx == last_idx:
                last_date = date
                break
        
        if last_date:
            # Check if this is actually the final quarter of the year
            # Get all dates for this year
            year_dates = [d for idx, d in valid_dates if d.year == last_date.year]
            if year_dates:
                actual_last_quarter = max(year_dates)
                if last_date != actual_last_quarter:
                    # Remove the final label if it's not the true final quarter
                    tickvals.pop()
                    ticktext.pop()
                    labeled_indices.discard(last_idx)
    
    # Check if the final label follows the same spacing pattern as other labels
    if len(tickvals) > 2:
        # Calculate the typical spacing between labels
        spacings = []
        for i in range(1, len(tickvals)):
            spacing = tickvals[i] - tickvals[i-1]
            spacings.append(spacing)
        
        if spacings:
            # Calculate average spacing (excluding the last interval)
            avg_spacing = sum(spacings[:-1]) / len(spacings[:-1]) if len(spacings) > 1 else spacings[0]
            
            # Check if the final spacing is significantly different from average
            final_spacing = spacings[-1] if spacings else 0
            if abs(final_spacing - avg_spacing) > avg_spacing * 0.5:  # If more than 50% different
                # Remove the final label as it doesn't follow the pattern
                tickvals.pop()
                ticktext.pop()
                labeled_indices.discard(tickvals[-1] if tickvals else None)
    
    # Add all quarterly points for tick marks, but only show labels for final quarters
    all_quarterly_indices = [idx for idx, date in valid_dates]
    all_quarterly_texts = []
    
    for idx, date in valid_dates:
        if idx in labeled_indices:
            all_quarterly_texts.append(f"{MONTH_NAMES[date.month]} {date.year}")
        else:
            all_quarterly_texts.append("")  # Empty text for unlabeled ticks
    
    return {
        'tickmode': 'array',
        'tickvals': tickvals,
        'ticktext': ticktext,
        'tickangle': 0,
        'showticklabels': True,
        'showgrid': False,
        'ticks': 'outside',
        'ticklen': 8,
        'tickwidth': 2,
        'tickcolor': 'black',
        'showline': True,
        'linecolor': 'black',
        'linewidth': 1,
        'minor': {
            'tickmode': 'array',
            'tickvals': all_quarterly_indices,
            'showgrid': False,
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 1,
            'tickcolor': 'black'
        }
    }

def apply_yearly_spacing(dates, x_labels):
    """Show evenly spaced years: 2, 4, 5, 10, 20, 50, 100 year intervals"""
    if len(dates) < 2:
        return apply_default_spacing(x_labels)
    
    # Find year range
    valid_dates = [d for d in dates if d]
    if len(valid_dates) < 2:
        return apply_default_spacing(x_labels)
    
    min_year = min(d.year for d in valid_dates)
    max_year = max(d.year for d in valid_dates)
    year_span = max_year - min_year
    
    # Choose appropriate spacing
    if year_span <= 5:
        spacing = 1
    elif year_span <= 20:
        spacing = 2
    elif year_span <= 50:
        spacing = 5
    elif year_span <= 100:
        spacing = 10
    else:
        spacing = 20
    
    tickvals = []
    ticktext = []
    
    for i, (date, label) in enumerate(zip(dates, x_labels)):
        if date and (date.year - min_year) % spacing == 0:
            tickvals.append(i)
            ticktext.append(str(date.year))
    
    # Check if the final label follows the same spacing pattern as other labels
    if len(tickvals) > 2:
        # Calculate the typical spacing between labels
        spacings = []
        for i in range(1, len(tickvals)):
            spacing = tickvals[i] - tickvals[i-1]
            spacings.append(spacing)
        
        if spacings:
            # Calculate average spacing (excluding the last interval)
            avg_spacing = sum(spacings[:-1]) / len(spacings[:-1]) if len(spacings) > 1 else spacings[0]
            
            # Check if the final spacing is significantly different from average
            final_spacing = spacings[-1] if spacings else 0
            if abs(final_spacing - avg_spacing) > avg_spacing * 0.5:  # If more than 50% different
                # Remove the final label as it doesn't follow the pattern
                tickvals.pop()
                ticktext.pop()
    
    return {
        'tickmode': 'array',
        'tickvals': tickvals,
        'ticktext': ticktext,
        'tickangle': 0,
        'showticklabels': True,
        'showgrid': False,
        'ticks': 'outside',
        'ticklen': 8,
        'tickwidth': 2,
        'tickcolor': 'black',
        'showline': True,
        'linecolor': 'black',
        'linewidth': 1
    }

def apply_default_spacing(x_labels):
    """Default spacing for non-time-series data"""
    if len(x_labels) <= 20:
        return {}  # No spacing needed
    
    # Show every nth label
    n = max(1, len(x_labels) // 10)
    tickvals = list(range(0, len(x_labels), n))
    ticktext = [x_labels[i] for i in tickvals]
    
    return {
        'tickmode': 'array',
        'tickvals': tickvals,
        'ticktext': ticktext,
        'tickangle': 45
    }

# Register API routes
register_quarterly_stats_routes(app)

if __name__ == '__main__':
    print("🚀 Starting GetCharty Local Server...")
    print("📊 Server will be available at: http://localhost:5000")
    print("🌐 Client will be available at: http://localhost:8000")
    print("📁 Upload your CSV files to see the magic!")
    app.run(debug=True, host='0.0.0.0', port=5000) 