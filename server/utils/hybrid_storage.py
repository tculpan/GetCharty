# hybrid_storage.py
# 2025-07-28 17:50:00 UTC
# Hybrid storage manager for in-memory and database file storage

from collections import defaultdict, deque
import pandas as pd
import io
import json
import uuid
import sqlite3
from datetime import datetime
from models import get_session

class HybridStorageManager:
    def __init__(self, max_files_per_user=3):
        # In-memory storage: {user_id: deque([(file_id, DataFrame), ...], maxlen=max_files_per_user)}
        self.in_memory_files = defaultdict(lambda: deque(maxlen=max_files_per_user))
        self.max_files_per_user = max_files_per_user
    
    def store_file(self, user_id, file_content, filename):
        """Store a file using hybrid approach - recent files in memory, older in DB"""
        file_id = str(uuid.uuid4())
        
        # Process the file content
        df = pd.read_csv(io.StringIO(file_content))
        file_size = len(file_content.encode('utf-8'))
        total_records = len(df)
        columns_json = json.dumps(list(df.columns))
        
        # Check if we need to move oldest file to database
        if len(self.in_memory_files[user_id]) == self.max_files_per_user:
            self._move_oldest_to_db(user_id)
        
        # Add new file to memory
        self.in_memory_files[user_id].append((file_id, df))
        
        # Also store in database for persistence
        self._store_in_db(file_id, user_id, filename, file_content, file_size, total_records, columns_json)
        
        return file_id
    
    def get_file_df(self, user_id, file_id):
        """Get a file DataFrame - check memory first, then database"""
        # Check in-memory first
        for fid, df in self.in_memory_files[user_id]:
            if fid == file_id:
                return df
        
        # If not in memory, load from database
        return self._load_from_db(user_id, file_id)
    
    def get_user_files(self, user_id):
        """Get list of files for a user (both in-memory and database)"""
        files = []
        
        # Add in-memory files
        for file_id, df in self.in_memory_files[user_id]:
            files.append({
                'file_id': file_id,
                'filename': f"Recent: {len(df)} records",
                'in_memory': True,
                'total_records': len(df),
                'columns': list(df.columns)
            })
        
        # Add database files
        conn = get_session()
        cursor = conn.cursor()
        cursor.execute('SELECT file_id, filename, total_records, columns, upload_date FROM files WHERE user_id = ?', (user_id,))
        db_files = cursor.fetchall()
        
        for file_record in db_files:
            file_id, filename, total_records, columns_json, upload_date = file_record
            # Skip if already in memory
            if not any(fid == file_id for fid, _ in self.in_memory_files[user_id]):
                files.append({
                    'file_id': file_id,
                    'filename': filename,
                    'in_memory': False,
                    'total_records': total_records,
                    'columns': json.loads(columns_json),
                    'upload_date': upload_date
                })
        
        conn.close()
        return files
    
    def _move_oldest_to_db(self, user_id):
        """Move the oldest file from memory to database"""
        if len(self.in_memory_files[user_id]) > 0:
            # The oldest file is at the beginning of the deque
            # It's already in the database, so we just remove it from memory
            self.in_memory_files[user_id].popleft()
    
    def _store_in_db(self, file_id, user_id, filename, file_content, file_size, total_records, columns_json):
        """Store file in database"""
        conn = get_session()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO files (file_id, user_id, filename, data, file_size, total_records, columns)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (file_id, user_id, filename, file_content.encode('utf-8'), file_size, total_records, columns_json))
        conn.commit()
        conn.close()
    
    def _load_from_db(self, user_id, file_id):
        """Load file from database"""
        conn = get_session()
        cursor = conn.cursor()
        cursor.execute('SELECT data FROM files WHERE file_id = ? AND user_id = ?', (file_id, user_id))
        record = cursor.fetchone()
        
        if record:
            # Decode the data and create DataFrame
            file_content = record[0].decode('utf-8')
            df = pd.read_csv(io.StringIO(file_content))
            
            # Move this file to memory (evicting oldest if needed)
            if len(self.in_memory_files[user_id]) == self.max_files_per_user:
                self.in_memory_files[user_id].popleft()
            self.in_memory_files[user_id].append((file_id, df))
            
            conn.close()
            return df
        
        conn.close()
        return None
    
    def delete_file(self, user_id, file_id):
        """Delete a file from both memory and database"""
        # Remove from memory
        self.in_memory_files[user_id] = deque(
            [(fid, df) for fid, df in self.in_memory_files[user_id] if fid != file_id],
            maxlen=self.max_files_per_user
        )
        
        # Remove from database
        conn = get_session()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM files WHERE file_id = ? AND user_id = ?', (file_id, user_id))
        conn.commit()
        conn.close()

# Global storage manager instance
storage_manager = HybridStorageManager() 