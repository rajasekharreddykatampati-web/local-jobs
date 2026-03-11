from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from ..database import get_db
from ..models import User, WorkerProfile, Review
from ..auth import get_current_user

router = APIRouter(prefix="/api/workers", tags=["workers"])

class WorkerProfileCreate(BaseModel):
    phone: str
    service_type: str
    experience: int
    location: str
    description: Optional[str] = ""
    profile_image: Optional[str] = ""

class WorkerProfileResponse(WorkerProfileCreate):
    id: int
    user_id: int
    is_approved: bool
    
    class Config:
        from_attributes = True

class WorkerSearchResponse(WorkerProfileResponse):
    name: str
    email: str

@router.post("/profile", response_model=WorkerProfileResponse)
def create_profile(profile: WorkerProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(WorkerProfile).filter(WorkerProfile.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    # Ensure role is worker
    if current_user.role != "worker":
        current_user.role = "worker"
        
    db_profile = WorkerProfile(**profile.model_dump(), user_id=current_user.id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/", response_model=List[WorkerSearchResponse])
def search_workers(
    service_type: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(WorkerProfile, User.name, User.email).join(User, WorkerProfile.user_id == User.id).filter(WorkerProfile.is_approved == True)
    
    if service_type:
        query = query.filter(WorkerProfile.service_type.ilike(f"%{service_type}%"))
    if location:
        query = query.filter(WorkerProfile.location.ilike(f"%{location}%"))
        
    results = query.all()
    
    response = []
    for profile, name, email in results:
        prof_dict = {c.name: getattr(profile, c.name) for c in profile.__table__.columns}
        prof_dict["name"] = name or "Unknown"
        prof_dict["email"] = email
        response.append(prof_dict)
        
    return response

@router.get("/{worker_id}", response_model=WorkerSearchResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    result = db.query(WorkerProfile, User.name, User.email).join(User, WorkerProfile.user_id == User.id).filter(WorkerProfile.id == worker_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Worker not found")
        
    profile, name, email = result
    prof_dict = {c.name: getattr(profile, c.name) for c in profile.__table__.columns}
    prof_dict["name"] = name or "Unknown"
    prof_dict["email"] = email
    return prof_dict
