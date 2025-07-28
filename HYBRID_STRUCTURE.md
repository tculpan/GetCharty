# GetCharty Hybrid Storage File Structure

## Overview
This document outlines the file structure for the GetCharty hybrid storage system that combines in-memory and database storage.

## File Structure

```
GetCharty/
├── client/
│   ├── index.html              # Updated client with session management and file UI
│   └── server.py               # Custom HTTP server for client
├── server/
│   ├── app.py                  # Updated Flask app with hybrid storage endpoints
│   ├── models.py               # NEW: SQLAlchemy database models
│   ├── init_db.py              # NEW: Database initialization script
│   ├── requirements.txt        # Updated with SQLAlchemy dependency
│   ├── config.py               # Date formats and quarter definitions
│   ├── schema.sql              # Database schema (legacy)
│   ├── getcharty.db           # SQLite database file (auto-created)
│   ├── api/
│   │   ├── quarterly_stats.py  # Updated to work with hybrid storage
│   │   └── validate_dates.py   # Date validation utilities
│   └── utils/
│       ├── hybrid_storage.py   # NEW: Hybrid storage manager
│       ├── user_manager.py     # NEW: User session management
│       ├── data_processor.py   # Updated to work with DataFrames
│       └── cache_manager.py    # Redis cache manager (optional)
├── start-local.bat            # Updated Windows startup script
├── start-local.sh             # Updated Linux/macOS startup script
├── README.md                  # Project documentation
└── HYBRID_STRUCTURE.md       # This file
```

## Key Changes Made

### 1. New Files Created
- **`server/models.py`**: SQLAlchemy models for database storage
- **`server/utils/hybrid_storage.py`**: Hybrid storage manager implementation
- **`server/utils/user_manager.py`**: User session management
- **`server/init_db.py`**: Database initialization script
- **`HYBRID_STRUCTURE.md`**: This documentation file

### 2. Updated Files
- **`server/app.py`**: Added hybrid storage endpoints and user management
- **`server/requirements.txt`**: Added SQLAlchemy dependency
- **`server/api/quarterly_stats.py`**: Updated to work with hybrid storage
- **`server/utils/data_processor.py`**: Updated to work with DataFrames
- **`client/index.html`**: Added session management and file management UI
- **`start-local.bat`**: Added database initialization step
- **`start-local.sh`**: Added database initialization step

### 3. Key Features Implemented

#### Hybrid Storage System
- **In-Memory**: Last 3 files per user stored in RAM for fast access
- **Database**: All files stored in SQLite for persistence
- **Automatic Migration**: Oldest files moved from memory to database when limit reached

#### User Management
- **Session-based**: Users identified by session ID stored in localStorage
- **Automatic User Creation**: New users created automatically on first file upload
- **Session Persistence**: User sessions stored in database with timeout

#### File Management
- **Upload**: Files processed server-side and stored in hybrid system
- **List**: Display all user files with storage location indicators
- **Load**: Load files from memory or database
- **Delete**: Remove files from both memory and database

#### API Endpoints
- `POST /process-file`: Upload and process files
- `GET /api/files`: List user files
- `GET /api/files/<file_id>`: Load specific file
- `DELETE /api/files/<file_id>`: Delete file
- `POST /api/quarterly-stats`: Get quarterly statistics

## Database Schema

### Files Table
```sql
CREATE TABLE files (
    file_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    data BLOB NOT NULL,
    file_size INTEGER NOT NULL,
    total_records INTEGER NOT NULL,
    columns TEXT NOT NULL
);
```

### User Sessions Table
```sql
CREATE TABLE user_sessions (
    session_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Usage Instructions

1. **Start the application**:
   ```bash
   # Windows
   start-local.bat
   
   # Linux/macOS
   ./start-local.sh
   ```

2. **Access the application**:
   - Client: http://localhost:8000
   - API: http://localhost:5000

3. **Upload files**: Files are automatically stored in the hybrid system

4. **View files**: The "Your Files" section shows all uploaded files with storage indicators

5. **Load files**: Click "Load" to retrieve files from memory or database

## Benefits

- **Performance**: Recent files load instantly from memory
- **Persistence**: All files saved to database, no data loss
- **Scalability**: Memory usage limited to 3 files per user
- **User Experience**: Seamless file management with visual indicators
- **Cost Effective**: Minimal database usage for active files

## Technical Details

- **Memory Limit**: 3 files per user in RAM
- **Session Timeout**: 24 hours of inactivity
- **Database**: SQLite for simplicity and portability
- **File Format**: CSV content stored as binary in database
- **User Identification**: Session-based with automatic user creation 