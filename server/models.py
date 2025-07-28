# models.py
# 2025-07-28 17:50:00 UTC
# Database models for hybrid in-memory/database file storage

import sqlite3
import json
from datetime import datetime
import uuid

def init_database():
    """Initialize the database and create tables"""
    conn = sqlite3.connect('getcharty.db')
    cursor = conn.cursor()
    
    # Create files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data BLOB NOT NULL,
            file_size INTEGER NOT NULL,
            total_records INTEGER NOT NULL,
            columns TEXT NOT NULL
        )
    ''')
    
    # Create user_sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")
    print("📁 Database file: getcharty.db")
    print("🗂️  Tables created: files, user_sessions")

def get_session():
    """Get a database connection"""
    return sqlite3.connect('getcharty.db')

class FileRecord:
    def __init__(self, file_id, user_id, filename, data, file_size, total_records, columns):
        self.file_id = file_id
        self.user_id = user_id
        self.filename = filename
        self.data = data
        self.file_size = file_size
        self.total_records = total_records
        self.columns = columns

class UserSession:
    def __init__(self, session_id, user_id):
        self.session_id = session_id
        self.user_id = user_id 