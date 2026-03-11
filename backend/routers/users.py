from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import User
from ..auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    role: Optional[str] = "user"

class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    role: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class FirebaseLogin(BaseModel):
    firebase_token: str
    email: str
    name: str = ""
    uid: str

@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, name=user.name, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/firebase-login", response_model=Token)
def firebase_login(login_data: FirebaseLogin, db: Session = Depends(get_db)):
    # If a user logs in via Firebase Google Sign in, trust the provided email/uid for this application
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        user = User(email=login_data.email, name=login_data.name, firebase_uid=login_data.uid, role="user")
        db.add(user)
        db.commit()
        db.refresh(user)
    elif not user.firebase_uid:
        user.firebase_uid = login_data.uid
        db.commit()
        
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
