# user_manager.py
# 2025-07-28 17:50:00 UTC
# User session management for hybrid storage system

import uuid
import sqlite3
from datetime import datetime, timedelta
from models import get_session

class UserManager:
    def __init__(self):
        self.session_timeout = timedelta(hours=24)  # 24 hour session timeout
    
    def get_or_create_user_id(self, session_id=None):
        """Get or create a user ID from session"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        conn = get_session()
        cursor = conn.cursor()
        
        # Check if session exists and is valid
        cursor.execute('SELECT user_id FROM user_sessions WHERE session_id = ?', (session_id,))
        result = cursor.fetchone()
        
        if result:
            # Update last activity
            cursor.execute('UPDATE user_sessions SET last_activity = CURRENT_TIMESTAMP WHERE session_id = ?', (session_id,))
            conn.commit()
            user_id = result[0]
        else:
            # Create new user session
            user_id = str(uuid.uuid4())
            cursor.execute('INSERT INTO user_sessions (session_id, user_id) VALUES (?, ?)', (session_id, user_id))
            conn.commit()
        
        conn.close()
        return user_id
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions from database"""
        conn = get_session()
        cursor = conn.cursor()
        
        # SQLite doesn't have a direct way to subtract timedelta, so we'll use a simpler approach
        # For now, we'll just delete sessions older than 24 hours
        cursor.execute('DELETE FROM user_sessions WHERE last_activity < datetime("now", "-24 hours")')
        conn.commit()
        conn.close()
    
    def get_user_from_session(self, session_id):
        """Get user ID from session ID"""
        conn = get_session()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM user_sessions WHERE session_id = ?', (session_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None

# Global user manager instance
user_manager = UserManager() 