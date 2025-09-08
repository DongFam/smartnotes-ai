from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Model for Notes
class Note(Base):
    __tablename__ = "notes"

    # Primary key
    id = mapped_column(Integer, primary_key=True)
    
    # Foreign key
    notebook_id = mapped_column(Integer, ForeignKey("notebooks.id"), nullable=False, index=True)
    
    # Core content
    title = mapped_column(String(200), nullable=False)
    content = mapped_column(Text, nullable=True)  # OCR/text content
    
    # Stroke data (PencilKit)
    stroke_data = mapped_column(JSON, nullable=True)  # Current enhanced strokes
    original_stroke_data = mapped_column(JSON, nullable=True)  # Preserve original handwriting
    
    # Enhancement tracking
    thumbnail_url = mapped_column(String(500), nullable=True)
    is_enhanced = mapped_column(Boolean, default=False)
    enhancement_status = mapped_column(String(20), default='pending')  # pending/processing/completed/failed
    enhancement_version = mapped_column(Integer, default=0, index=True)  # Current enhancement version
    
    # Status flags
    is_archived = mapped_column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    notebook = relationship("Notebook", back_populates="notes")
    enhancements = relationship("Enhancement", back_populates="note", cascade="all, delete-orphan", order_by="Enhancement.version")