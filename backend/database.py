import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env") # Since database.py is in backend, .env is in root

SQLALCHEMY_DATABASE_URL = os.getenv("SUPABASE_URL")

# Supabase URL usually starts with postgresql://, which SQLAlchemy handles automatically with psycopg2
try:
    if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Error configuring database: {e}")
    # Fallback to prevent app crash if .env not loaded during simple imports
    engine = None
    SessionLocal = None
    Base = declarative_base()

def get_db():
    if SessionLocal is None:
        raise Exception("Database not configured. Check SUPABASE_URL in .env")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
