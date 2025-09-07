from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Model for Notes
class Note(Base):
    __tablename__ = "notes"

    # Column names
    id = mapped_column(Integer, primary_key=True)
    notebook_id = mapped_column(Integer, ForeignKey("notebooks.id"))
    title = mapped_column(String(200), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with enhancement, creating a connection with enhancement table. 
    # If notes are deleted, all enhancements are deleted too
    enhancement = relationship("Enhancement", back_populates="note", cascade="all, delete-orphan")