"""
Database configuration and session management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Fix: Remove "DATABASE_URL=" prefix if present (Render sometimes includes it in the value)
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("DATABASE_URL="):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("DATABASE_URL=", "", 1).strip()

# Validate DATABASE_URL exists
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please set it in Render Dashboard → Environment Variables.")

# For Supabase/PostgreSQL, ensure SSL is enabled
# If DATABASE_URL doesn't have ?sslmode=require, add it
if SQLALCHEMY_DATABASE_URL and "supabase" in SQLALCHEMY_DATABASE_URL.lower():
    if "sslmode" not in SQLALCHEMY_DATABASE_URL:
        # Add SSL mode if not present
        separator = "&" if "?" in SQLALCHEMY_DATABASE_URL else "?"
        SQLALCHEMY_DATABASE_URL = f"{SQLALCHEMY_DATABASE_URL}{separator}sslmode=require"

# Create engine with connection pooling and SSL support
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=300,    # Recycle connections after 5 minutes
    connect_args={
        "sslmode": "require" if "supabase" in (SQLALCHEMY_DATABASE_URL or "").lower() else None
    } if SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


