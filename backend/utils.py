"""
Utility functions for Adumuo
"""

from datetime import datetime
from sqlalchemy.orm import Session
from models import Complaint


def generate_ref_id(db: Session) -> str:
    """
    Generate a unique reference ID in format: MPM-2025-XXXX
    Where XXXX is a 4-digit sequential number
    """
    current_year = datetime.now().year
    
    # Get the highest ref_id number for this year
    last_complaint = db.query(Complaint).filter(
        Complaint.ref_id.like(f"MPM-{current_year}-%")
    ).order_by(Complaint.id.desc()).first()
    
    if last_complaint:
        # Extract the number from the last ref_id
        try:
            last_number = int(last_complaint.ref_id.split("-")[-1])
            next_number = last_number + 1
        except (ValueError, IndexError):
            next_number = 1
    else:
        next_number = 1
    
    # Format as 4-digit number with leading zeros
    ref_id = f"MPM-{current_year}-{next_number:04d}"
    
    return ref_id

