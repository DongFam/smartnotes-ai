from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Model for enhanced notes
class Enhancement(Base):
    __tablename__ = "enhancements"

    # Column names
    id = mapped_column(Integer, primary_key=True)
    note_id = mapped_column(Integer, ForeignKey("notes.id"), nullable=False)
    original_url = mapped_column(String(500), nullable=False)
    enhanced_url = mapped_column(String(500), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

