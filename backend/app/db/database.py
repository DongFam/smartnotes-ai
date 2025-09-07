import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings


# Takes the URL to create an engine (Connections to PostgreSQL)
engine = create_engine(
    settings.DATABASE_URL,
    pool_size = settings.DB_POOL_SIZE,
    max_overflow = settings.DB_MAX_OVERFLOW,
    pool_timeout = settings.DB_POOL_TIMEOUT,
    echo = settings.DB_ECHO)

# Creates a session using the engine to connect to the DB
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)

# Model inheritance
Base = declarative_base()

# Creates a session and closes it when done (Use at the start of a logical unit of work: 
# a web request, a CLI command, a background job, or a user action in a GUI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(bind=engine)