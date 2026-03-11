from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ..models import User, Message
from ..auth import get_current_user

router = APIRouter(prefix="/api/messages", tags=["messages"])

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=MessageResponse)
def send_message(msg: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if receiver exists
    receiver = db.query(User).filter(User.id == msg.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
        
    db_msg = Message(sender_id=current_user.id, receiver_id=msg.receiver_id, content=msg.content)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

@router.get("/{other_user_id}", response_model=List[MessageResponse])
def get_chat_history(other_user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = db.query(Message).filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == other_user_id),
            and_(Message.sender_id == other_user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()
    
    return messages
