from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import engine, Base

try:
    if engine:
        Base.metadata.create_all(bind=engine)
except Exception as e:
    print("Warning: Database might not be connected correctly:", e)

app = FastAPI(title="Local Link Services API")

# Setup CORS to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this to the frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routers import users, workers, admin, messages

@app.get("/")
def read_root():
    return {"message": "Welcome to Local Link Services API"}

app.include_router(users.router)
app.include_router(workers.router)
app.include_router(admin.router)
app.include_router(messages.router)
