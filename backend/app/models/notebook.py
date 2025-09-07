from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Notebook(Base):
    __tablename__ = "notebooks"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    name = mapped_column(String(200), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    notes = relationship("Note", back_populates="notebook", cascade="all, delete-orphan")

