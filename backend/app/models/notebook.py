from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Notebook(Base):
    __tablename__ = "notebooks"

    # Primary key
    id = mapped_column(Integer, primary_key=True)
    
    # Foreign key
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Core content
    name = mapped_column(String(200), nullable=False)
    description = mapped_column(Text, nullable=True)
    
    # UI customization
    color = mapped_column(String(7), default='#000000')  # hex color codes
    
    # Status flags
    is_archived = mapped_column(Boolean, default=False, index=True)
    is_favorite = mapped_column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="notebooks")
    notes = relationship("Note", back_populates="notebook", cascade="all, delete-orphan")

