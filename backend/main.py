"""
Adumuo (Aduan Rakyat Muo) - FastAPI Backend
Municipal Complaint System for Majlis Perbandaran Muar
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import uvicorn
import os
import shutil
from pathlib import Path

from database import SessionLocal, engine, Base
from models import Complaint
from schemas import ComplaintCreate, ComplaintResponse, ComplaintStatusResponse, AdminLogin, StatusUpdate
from utils import generate_ref_id
from auth import verify_token, create_access_token, ADMIN_USERNAME, ADMIN_PASSWORD

# Create database tables
Base.metadata.create_all(bind=engine)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Adumuo API",
    description="Municipal Complaint System API for Majlis Perbandaran Muar",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Adumuo API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.post("/api/complaints", response_model=ComplaintResponse, status_code=201)
async def create_complaint(
    citizen_name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    image_file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Create a new complaint.
    Accepts complaint data with optional image upload or URL.
    Generates a unique Reference ID.
    Compatible with n8n webhook integration.
    """
    try:
        # Generate unique reference ID
        ref_id = generate_ref_id(db)
        
        # Handle image upload
        final_image_url = image_url
        
        if image_file and image_file.filename:
            # Save uploaded file
            file_ext = Path(image_file.filename).suffix
            file_path = UPLOAD_DIR / f"{ref_id}{file_ext}"
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
            
            # In production, upload to cloud storage and get URL
            # For now, return relative path
            final_image_url = f"/uploads/{ref_id}{file_ext}"
        
        # Create complaint record
        db_complaint = Complaint(
            ref_id=ref_id,
            citizen_name=citizen_name,
            category=category,
            description=description,
            image_url=final_image_url,
            latitude=latitude,
            longitude=longitude,
            status="Pending"
        )
        
        db.add(db_complaint)
        db.commit()
        db.refresh(db_complaint)
        
        return ComplaintResponse(
            id=db_complaint.id,
            ref_id=db_complaint.ref_id,
            citizen_name=db_complaint.citizen_name,
            category=db_complaint.category,
            description=db_complaint.description,
            image_url=db_complaint.image_url,
            latitude=db_complaint.latitude,
            longitude=db_complaint.longitude,
            status=db_complaint.status,
            created_at=db_complaint.created_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating complaint: {str(e)}")


@app.get("/api/complaints/{ref_id}", response_model=ComplaintStatusResponse)
async def get_complaint_status(
    ref_id: str,
    db: Session = Depends(get_db)
):
    """
    Fetch complaint status by Reference ID.
    Returns complaint details with current status.
    """
    complaint = db.query(Complaint).filter(Complaint.ref_id == ref_id).first()
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    return ComplaintStatusResponse(
        ref_id=complaint.ref_id,
        citizen_name=complaint.citizen_name,
        category=complaint.category,
        description=complaint.description,
        image_url=complaint.image_url,
        status=complaint.status,
        created_at=complaint.created_at
    )


@app.get("/api/complaints", response_model=list[ComplaintResponse])
async def list_complaints(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all complaints (for admin/internal use).
    Supports pagination.
    """
    complaints = db.query(Complaint).offset(skip).limit(limit).all()
    return complaints


# Admin Endpoints
@app.post("/api/admin/login")
async def admin_login(credentials: AdminLogin):
    """
    Admin login endpoint.
    Returns JWT token for authenticated requests.
    """
    # Simple authentication (in production, use database)
    if credentials.username == ADMIN_USERNAME and credentials.password == ADMIN_PASSWORD:
        access_token = create_access_token(data={"sub": credentials.username})
        return {"token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


@app.get("/api/admin/complaints", response_model=list[ComplaintResponse])
async def admin_list_complaints(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    username: str = Depends(verify_token)
):
    """
    List all complaints for admin dashboard.
    Requires authentication.
    """
    complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).offset(skip).limit(limit).all()
    return complaints


@app.patch("/api/admin/complaints/{ref_id}", response_model=ComplaintResponse)
async def admin_update_complaint_status(
    ref_id: str,
    status_update: StatusUpdate,
    db: Session = Depends(get_db),
    username: str = Depends(verify_token)
):
    """
    Update complaint status (Pending, Assigned, Resolved).
    Requires authentication.
    """
    complaint = db.query(Complaint).filter(Complaint.ref_id == ref_id).first()
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Validate status
    valid_statuses = ["Pending", "Assigned", "Resolved"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {', '.join(valid_statuses)}")
    
    complaint.status = status_update.status
    db.commit()
    db.refresh(complaint)
    
    return ComplaintResponse(
        id=complaint.id,
        ref_id=complaint.ref_id,
        citizen_name=complaint.citizen_name,
        category=complaint.category,
        description=complaint.description,
        image_url=complaint.image_url,
        latitude=complaint.latitude,
        longitude=complaint.longitude,
        status=complaint.status,
        created_at=complaint.created_at
    )


# Serve uploaded files
@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    """Serve uploaded complaint images"""
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        from fastapi.responses import FileResponse
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

