--6. Database Schema Updates (if using a database)

-- Add tables for storing file metadata
CREATE TABLE file_metadata (
    id UUID PRIMARY KEY,
    filename VARCHAR(255),
    upload_date TIMESTAMP,
    date_columns JSON,
    date_range JSON,
    total_records INTEGER
);

-- Add table for caching quarterly summaries
CREATE TABLE quarterly_summaries (
    id UUID PRIMARY KEY,
    file_id UUID REFERENCES file_metadata(id),
    year INTEGER,
    quarter INTEGER,
    summary_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);