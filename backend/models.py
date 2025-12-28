"""
SQLAlchemy database models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class Complaint(Base):
    """Complaint model for storing citizen complaints"""
    
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    ref_id = Column(String(50), unique=True, index=True, nullable=False)
    citizen_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String(50), default="Pending", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)



