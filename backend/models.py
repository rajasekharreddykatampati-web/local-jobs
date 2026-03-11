from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    role = Column(String, default="user") # 'user', 'worker', 'admin'
    firebase_uid = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    worker_profile = relationship("WorkerProfile", back_populates="user", uselist=False)
    reviews_given = relationship("Review", back_populates="reviewer", foreign_keys="Review.reviewer_id")
    messages_sent = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    messages_received = relationship("Message", back_populates="receiver", foreign_keys="Message.receiver_id")

class WorkerProfile(Base):
    __tablename__ = "worker_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    phone = Column(String, nullable=True)
    service_type = Column(String, index=True)
    experience = Column(Integer, nullable=True) # in years
    location = Column(String, index=True)
    description = Column(Text, nullable=True)
    profile_image = Column(String, nullable=True)
    is_approved = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="worker_profile")
    reviews_received = relationship("Review", back_populates="worker", foreign_keys="Review.worker_id")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("worker_profiles.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Float)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    worker = relationship("WorkerProfile", back_populates="reviews_received", foreign_keys=[worker_id])
    reviewer = relationship("User", back_populates="reviews_given", foreign_keys=[reviewer_id])

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User", back_populates="messages_sent", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="messages_received", foreign_keys=[receiver_id])
