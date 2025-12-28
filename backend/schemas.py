"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ComplaintCreate(BaseModel):
    """Schema for creating a new complaint"""
    
    citizen_name: str = Field(..., min_length=1, max_length=255, description="Name of the citizen")
    category: str = Field(..., min_length=1, max_length=100, description="Complaint category")
    description: str = Field(..., min_length=10, description="Detailed description of the complaint")
    image_url: Optional[str] = Field(None, max_length=500, description="URL to complaint image")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "citizen_name": "Ahmad bin Abdullah",
                "category": "Infrastructure",
                "description": "Pothole on Jalan Abdullah, causing traffic issues",
                "image_url": "https://example.com/image.jpg",
                "latitude": 2.0442,
                "longitude": 102.5689
            }
        }


class ComplaintResponse(BaseModel):
    """Schema for complaint response"""
    
    id: int
    ref_id: str
    citizen_name: str
    category: str
    description: str
    image_url: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ComplaintStatusResponse(BaseModel):
    """Schema for complaint status lookup response"""
    
    ref_id: str
    citizen_name: str
    category: str
    description: str
    image_url: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    """Schema for admin login"""
    
    username: str
    password: str


class StatusUpdate(BaseModel):
    """Schema for updating complaint status"""
    
    status: str = Field(..., description="New status: Pending, Assigned, or Resolved")


