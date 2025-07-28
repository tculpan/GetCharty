# api/quarterly_stats.py
# 2025-07-28 17:50:00 UTC
# Updated to work with hybrid storage system

from flask import request, jsonify
from utils.hybrid_storage import storage_manager
from utils.user_manager import user_manager
from utils.data_processor import process_uploaded_file
import pandas as pd

def register_quarterly_stats_routes(app):
    """Register quarterly stats routes with the Flask app"""
    
    @app.route('/api/quarterly-stats', methods=['POST'])
    def get_quarterly_stats():
        """Get quarterly statistics for a file using hybrid storage"""
        try:
            data = request.json
            file_id = data.get('fileId')
            date_column = data.get('dateColumn')
            year = data.get('year')
            quarter = data.get('quarter')
            session_id = data.get('sessionId')
            
            # Get user ID
            user_id = user_manager.get_or_create_user_id(session_id)
            
            # Load data from hybrid storage
            df = storage_manager.get_file_df(user_id, file_id)
            
            if df is None:
                return jsonify({
                    'error': 'File not found'
                }), 404
            
            # Process dates and add quarter information
            if date_column and date_column in df.columns:
                df = process_uploaded_file(df, [date_column])
            
            # Filter by quarter
            if date_column and year and quarter:
                year_col = f'{date_column}_year'
                quarter_col = f'{date_column}_quarter'
                
                if year_col in df.columns and quarter_col in df.columns:
                    mask = (df[year_col] == year) & (df[quarter_col] == quarter)
                    df_filtered = df[mask]
                else:
                    df_filtered = df
            else:
                df_filtered = df
            
            # Calculate statistics
            stats = {
                'totalRecords': len(df_filtered),
                'numericColumns': {}
            }
            
            # Get stats for numeric columns
            numeric_cols = df_filtered.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                if col not in [date_column, f'{date_column}_year', f'{date_column}_quarter']:
                    stats['numericColumns'][col] = {
                        'sum': float(df_filtered[col].sum()),
                        'average': float(df_filtered[col].mean()),
                        'min': float(df_filtered[col].min()),
                        'max': float(df_filtered[col].max())
                    }
            
            return jsonify(stats)
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'message': 'Failed to get quarterly stats'
            }), 500

    @app.route('/api/quarterly-options', methods=['POST'])
    def get_quarterly_options():
        """Get available quarters for a file"""
        try:
            data = request.json
            file_id = data.get('fileId')
            date_column = data.get('dateColumn')
            session_id = data.get('sessionId')
            
            # Get user ID
            user_id = user_manager.get_or_create_user_id(session_id)
            
            # Load data from hybrid storage
            df = storage_manager.get_file_df(user_id, file_id)
            
            if df is None:
                return jsonify({
                    'error': 'File not found'
                }), 404
            
            # Process dates and add quarter information
            if date_column and date_column in df.columns:
                df = process_uploaded_file(df, [date_column])
                
                year_col = f'{date_column}_year'
                quarter_col = f'{date_column}_quarter'
                
                if year_col in df.columns and quarter_col in df.columns:
                    # Get unique year-quarter combinations
                    quarters = df[[year_col, quarter_col]].drop_duplicates().sort_values([year_col, quarter_col])
                    
                    options = []
                    for _, row in quarters.iterrows():
                        year = int(row[year_col])
                        quarter = int(row[quarter_col])
                        quarter_name = f"Q{quarter} {year}"
                        options.append({
                            'year': year,
                            'quarter': quarter,
                            'name': quarter_name
                        })
                    
                    return jsonify({
                        'availableQuarters': options,
                        'dateColumn': date_column
                    })
            
            return jsonify({
                'error': 'No date column found or processed'
            }), 400
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'message': 'Failed to get quarterly options'
            }), 500