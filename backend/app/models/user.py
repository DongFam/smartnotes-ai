from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Model for users
class User(Base):
    __tablename__ = "users"

    # Primary key
    id = mapped_column(Integer, primary_key=True)
    
    # User identification
    email = mapped_column(String(255), unique=True, nullable=False, index=True)
    username = mapped_column(String(50), unique=True, nullable=False, index=True)
    full_name = mapped_column(String(255), nullable=True)
    
    # Account status and subscription
    is_active = mapped_column(Boolean, default=True)
    subscription_tier = mapped_column(String(20), default='free', index=True)  # free/pro/team
    
    # Timestamps
    last_login = mapped_column(DateTime(timezone=True), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with notebooks (One to Many) 
    # If user is deleted, all notebooks are deleted too
    notebooks = relationship("Notebook", back_populates="user", cascade="all, delete-orphan")
