from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from fastapi import Depends
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL=os.getenv("DB_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()