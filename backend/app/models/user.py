from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Model for users
class User(Base):
    __tablename__ = "users"

    # Column names
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(255), unique=True, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationship with notes (One to Many) 
    # If user is deleted, all the notes are deleted too
    notebooks = relationship("Notebook", back_populates="user", cascade="all, delete-orphan")
