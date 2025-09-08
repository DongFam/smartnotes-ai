from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Model for enhancement history - tracks all enhancement versions
class Enhancement(Base):
    __tablename__ = "enhancements"

    # Primary key
    id = mapped_column(Integer, primary_key=True)
    
    # Foreign key
    note_id = mapped_column(Integer, ForeignKey("notes.id"), nullable=False, index=True)
    
    # Enhancement version tracking
    enhancement_type = mapped_column(String(20), nullable=False)  # beautify/ocr/shape/formula
    version = mapped_column(Integer, nullable=False, index=True)  # 1, 2, 3...
    is_current = mapped_column(Boolean, default=False, index=True)  # Only one per note
    
    # File URLs
    original_url = mapped_column(String(500), nullable=False)
    enhanced_url = mapped_column(String(500), nullable=False)
    
    # Processing metadata
    processing_time_ms = mapped_column(Integer, nullable=True)
    status = mapped_column(String(20), default='pending', index=True)  # pending/processing/completed/failed
    model_version = mapped_column(String(20), nullable=True)  # "beautify-v1.2"
    metadata = mapped_column(JSON, nullable=True)  # ML confidence scores, parameters, etc.
    
    # Timestamps
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    note = relationship("Note", back_populates="enhancements")

