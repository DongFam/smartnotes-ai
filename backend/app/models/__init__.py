# app/models/__init__.py
from app.models.user import User
from app.models.notebook import Notebook
from app.models.note import Note
from app.models.enhancement import Enhancement

# This allows: from app.models import User, Notebook, Note, Enhancement
__all__ = ["User", "Notebook", "Note", "Enhancement"]