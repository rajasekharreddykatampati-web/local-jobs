from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from ..database import get_db
from ..models import User, WorkerProfile
from ..auth import get_admin_user

router = APIRouter(prefix="/api/admin", tags=["admin"])

class AdminWorkerResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    service_type: str
    location: str
    is_approved: bool

@router.get("/users")
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "name": u.name, "role": u.role} for u in users]

@router.get("/workers", response_model=List[AdminWorkerResponse])
def get_all_workers(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    results = db.query(WorkerProfile, User.name, User.email).join(User, WorkerProfile.user_id == User.id).all()
    
    response = []
    for profile, name, email in results:
        response.append({
            "id": profile.id,
            "user_id": profile.user_id,
            "name": name or "Unknown",
            "email": email,
            "service_type": profile.service_type,
            "location": profile.location,
            "is_approved": profile.is_approved
        })
    return response

@router.put("/workers/{worker_id}/approve")
def approve_worker(worker_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    worker = db.query(WorkerProfile).filter(WorkerProfile.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    worker.is_approved = True
    db.commit()
    return {"status": "Approved"}

@router.delete("/workers/{worker_id}")
def remove_worker(worker_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    worker = db.query(WorkerProfile).filter(WorkerProfile.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    db.delete(worker)
    db.commit()
    return {"status": "Deleted"}
