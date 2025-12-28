-- Create complaints table for Adumuo
-- Run this SQL in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS complaints (
    id SERIAL PRIMARY KEY,
    ref_id VARCHAR(50) UNIQUE NOT NULL,
    citizen_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(500),
    latitude FLOAT,
    longitude FLOAT,
    status VARCHAR(50) DEFAULT 'Pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create index on ref_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_complaints_ref_id ON complaints(ref_id);

-- Create index on status for filtering
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_complaints_created_at ON complaints(created_at DESC);


