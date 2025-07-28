# init_db.py
# 2025-01-28 16:55:00
# Database initialization script for hybrid storage system

from models import init_database
import os

def init_database_tables():
    """Initialize the database and create all tables"""
    print("🔧 Initializing GetCharty database...")
    
    # Initialize database
    init_database()
    
    print("✅ Database initialized successfully!")
    print("📁 Database file: getcharty.db")
    print("🗂️  Tables created: files, user_sessions")

if __name__ == '__main__':
    init_database_tables() 