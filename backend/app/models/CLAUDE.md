# CLAUDE.md - SmartNote AI Models Reference

## Project Context

SmartNote AI is an iPad note-taking app with real-time handwriting beautification using hybrid on-device/cloud ML processing. This document serves as the definitive guide for database model development and maintenance.

## Architecture Overview

### Hybrid Processing Model
- **On-Device**: <50ms stroke smoothing, basic beautification, shape detection
- **Cloud**: 200-500ms advanced ML processing, OCR, formula recognition
- **Storage**: Original strokes preserved + versioned enhancements

### Tech Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0
- **Database**: PostgreSQL 17 (JSONB for stroke data)
- **Infrastructure**: DigitalOcean ($73/month budget)

## Database Schema Overview

### Core Entity Relationships

```
User (1) ──── (N) Notebook (1) ──── (N) Note (1) ──── (N) Enhancement
```

### Schema Design Principles

1. **Preserve Original Data**: Never lose user's original handwriting
2. **Version Everything**: Track all enhancement iterations
3. **Optimize for iPad**: Fast sync, offline-first design
4. **Cost-Conscious**: Efficient storage patterns
5. **ML-Friendly**: JSONB for flexible ML metadata

## Model Structure & Conventions

### Import Pattern
```python
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base
```

### Column Organization
1. **Primary Key**: Always `id` as first column
2. **Foreign Keys**: Group together after primary key
3. **Core Content**: Main data columns
4. **Metadata**: Flags, status, configuration
5. **Timestamps**: `created_at`, `updated_at` at end
6. **Relationships**: Always at bottom of class

### Naming Conventions
- **Tables**: Plural nouns (`users`, `notebooks`, `notes`, `enhancements`)
- **Columns**: Snake_case (`created_at`, `is_active`, `enhancement_version`)
- **Foreign Keys**: `{table_singular}_id` (`user_id`, `notebook_id`)
- **Booleans**: `is_` prefix (`is_active`, `is_enhanced`)
- **Status Fields**: `_status` suffix (`enhancement_status`)

### Standard Column Patterns

#### Timestamps (All Models)
```python
created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### Status Tracking
```python
# Use string enums for status fields
status = mapped_column(String(20), default='pending')  # pending/processing/completed/failed
```

#### Soft Delete Pattern
```python
is_archived = mapped_column(Boolean, default=False, index=True)
```

#### User Preferences
```python
is_favorite = mapped_column(Boolean, default=False, index=True)
```

## Current Models

### 1. User Model (`app/models/user.py`)

**Purpose**: Manages user authentication, subscription, and account data

**Current Columns**:
- `id`: Primary key
- `email`: Unique user identifier
- `created_at`: Account creation timestamp

**Missing Columns (To Add)**:
- `username`: Unique display name (String(50), unique, nullable=False, index=True)
- `full_name`: User's display name (String(255), nullable=True)
- `is_active`: Account status (Boolean, default=True)
- `subscription_tier`: Subscription level (String(20), default='free') # free/pro/team
- `last_login`: Last login timestamp (DateTime, nullable=True)
- `updated_at`: Account modification timestamp

**Relationships**:
- `notebooks`: One-to-Many with Notebook (cascade delete)

**Indexes Needed**:
- `email` (unique) ✓ exists
- `username` (unique) - add
- `subscription_tier` - add for billing queries

### 2. Notebook Model (`app/models/notebook.py`)

**Purpose**: Organizes notes into collections, like folders

**Current Columns**:
- `id`: Primary key
- `user_id`: Foreign key to User
- `name`: Notebook title
- `created_at`, `updated_at`: Timestamps

**Missing Columns (To Add)**:
- `description`: Optional description (Text, nullable=True)
- `color`: UI theme color (String(7), default='#000000') # hex colors
- `is_archived`: Soft delete flag (Boolean, default=False, index=True)
- `is_favorite`: User favorite flag (Boolean, default=False, index=True)

**Relationships**:
- `user`: Many-to-One with User
- `notes`: One-to-Many with Note (cascade delete)

**Indexes Needed**:
- `user_id` - add for user's notebooks
- `is_archived` - add for active notebooks
- `(user_id, is_archived)` - composite for filtered queries

### 3. Note Model (`app/models/note.py`)

**Purpose**: Individual note pages with handwriting and enhancements

**Current Columns**:
- `id`: Primary key
- `notebook_id`: Foreign key to Notebook
- `title`: Note title
- `created_at`, `updated_at`: Timestamps

**Missing Columns (To Add)**:
- `content`: OCR/text content (Text, nullable=True)
- `stroke_data`: Current stroke data (JSON) # PencilKit data
- `original_stroke_data`: Preserve original (JSON) # Never modified
- `thumbnail_url`: Preview image URL (String(500), nullable=True)
- `is_enhanced`: Has enhancements flag (Boolean, default=False)
- `enhancement_status`: Current status (String(20), default='pending')
- `enhancement_version`: Current version (Integer, default=0)
- `is_archived`: Soft delete flag (Boolean, default=False, index=True)

**Relationships**:
- `notebook`: Many-to-One with Notebook
- `enhancements`: One-to-Many with Enhancement (cascade delete, ordered by version)

**Indexes Needed**:
- `notebook_id` - add for notebook's notes
- `is_archived` - add for active notes
- `(notebook_id, is_archived)` - composite for filtered queries
- `enhancement_version` - add for version tracking

### 4. Enhancement Model (`app/models/enhancement.py`)

**Purpose**: Tracks all enhancement versions and ML processing history

**Current Columns**:
- `id`: Primary key
- `note_id`: Foreign key to Note
- `original_url`: Original image URL
- `enhanced_url`: Enhanced image URL
- `created_at`: Creation timestamp

**Missing Columns (To Add)**:
- `enhancement_type`: Type of enhancement (String(20), nullable=False) # beautify/ocr/shape/formula
- `version`: Enhancement version number (Integer, nullable=False) # 1, 2, 3...
- `processing_time_ms`: Performance tracking (Integer, nullable=True)
- `status`: Processing status (String(20), default='pending') # pending/processing/completed/failed
- `is_current`: Active version flag (Boolean, default=False) # Only one per note
- `model_version`: ML model used (String(20)) # "beautify-v1.2"
- `metadata`: Additional ML data (JSON) # confidence scores, etc.
- `updated_at`: Modification timestamp

**Enhancement Versioning System**:
- Version 0: Original user handwriting (no enhancement row)
- Version 1+: Each enhancement iteration gets new row
- `is_current=True`: Marks the version currently displayed
- All versions preserved for rollback capability

**Relationships**:
- `note`: Many-to-One with Note

**Indexes Needed**:
- `note_id` - add for note's enhancements
- `(note_id, version)` - composite for version lookups
- `(note_id, is_current)` - find active enhancement
- `status` - add for processing queue queries

## Performance Optimization

### Index Strategy

#### Primary Indexes (Essential)
```sql
-- User lookups
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Notebook queries
CREATE INDEX idx_notebooks_user_id ON notebooks(user_id);
CREATE INDEX idx_notebooks_archived ON notebooks(is_archived) WHERE is_archived = false;

-- Note queries
CREATE INDEX idx_notes_notebook_id ON notes(notebook_id);
CREATE INDEX idx_notes_archived ON notes(is_archived) WHERE is_archived = false;

-- Enhancement processing
CREATE INDEX idx_enhancements_note_id ON enhancements(note_id);
CREATE INDEX idx_enhancements_status ON enhancements(status) WHERE status != 'completed';
```

#### Composite Indexes (Performance)
```sql
-- User's active notebooks
CREATE INDEX idx_notebooks_user_active ON notebooks(user_id, is_archived);

-- Notebook's active notes
CREATE INDEX idx_notes_notebook_active ON notes(notebook_id, is_archived);

-- Enhancement versioning
CREATE UNIQUE INDEX idx_enhancements_note_version ON enhancements(note_id, version);
CREATE UNIQUE INDEX idx_enhancements_note_current ON enhancements(note_id) WHERE is_current = true;
```

### Query Patterns

#### Common Queries
```python
# User's active notebooks
notebooks = session.query(Notebook).filter(
    Notebook.user_id == user_id,
    Notebook.is_archived == False
).all()

# Notebook's notes with current enhancement
notes = session.query(Note).join(Enhancement, 
    and_(Enhancement.note_id == Note.id, Enhancement.is_current == True)
).filter(Note.notebook_id == notebook_id).all()

# Enhancement history for note
enhancements = session.query(Enhancement).filter(
    Enhancement.note_id == note_id
).order_by(Enhancement.version).all()
```

## Data Storage Patterns

### JSONB Usage

#### Stroke Data Structure
```json
{
  "strokes": [
    {
      "points": [[x1, y1, pressure1], [x2, y2, pressure2]],
      "timestamp": "2024-01-01T10:00:00Z",
      "tool": "pencil|pen|highlighter"
    }
  ],
  "canvas": {
    "width": 1024,
    "height": 1366,
    "scale": 1.0
  }
}
```

#### Enhancement Metadata
```json
{
  "ml_model": {
    "name": "beautify-v1.2",
    "confidence": 0.95,
    "processing_time": 250
  },
  "transformations": [
    {
      "type": "smooth",
      "parameters": {"strength": 0.3}
    },
    {
      "type": "straighten",
      "parameters": {"threshold": 0.8}
    }
  ]
}
```

### File Storage Strategy
- **Thumbnails**: Cloudflare R2 (CDN)
- **Original Images**: R2 with compression
- **Enhanced Images**: R2 with versioning
- **ML Models**: R2 with CDN distribution

## Development Guidelines

### Adding New Columns

1. **Add to Model**: Update model with new column
2. **Create Migration**: Use Alembic for schema changes
3. **Update Tests**: Add test coverage
4. **Update API**: Modify schemas and endpoints
5. **Consider Performance**: Add indexes if needed

### Model Changes Checklist

- [ ] Column added to model class
- [ ] Import statements updated if new types
- [ ] Relationship updated if foreign key
- [ ] Index added if performance critical
- [ ] Migration script created
- [ ] API schema updated
- [ ] Tests updated
- [ ] Documentation updated

### Error Handling Patterns

```python
# Relationship access with error handling
try:
    notebook = note.notebook
except AttributeError:
    logger.error(f"Note {note.id} missing notebook relationship")
    raise HTTPException(status_code=404, detail="Notebook not found")
```

### Cascade Behavior

- **User deleted**: All notebooks and notes cascade delete
- **Notebook deleted**: All notes cascade delete  
- **Note deleted**: All enhancements cascade delete
- **Enhancement deleted**: No cascade (history preserved)

## Cost Optimization

### Storage Efficiency
- **JSONB Compression**: Use PostgreSQL compression
- **Image Storage**: WebP format, progressive JPEG
- **Thumbnail Generation**: Multiple sizes cached
- **Old Version Cleanup**: Archive policy for enhancements

### Query Optimization
- **Eager Loading**: Use `joinedload()` for relationships
- **Pagination**: Limit query results
- **Caching**: Redis for frequent queries
- **Connection Pooling**: Configured in database.py

## Future Considerations

### Planned Features (Don't Implement Yet)
- **Collaboration**: User sharing, permissions
- **Templates**: Reusable note layouts  
- **Tags**: Multi-tag support with M2M relationship
- **Sync Conflicts**: Version resolution metadata
- **Analytics**: Usage tracking models

### Scaling Considerations
- **Partitioning**: Time-based partitioning for large tables
- **Read Replicas**: Separate read/write operations
- **Caching Layer**: Model-level caching
- **Archive Strategy**: Cold storage for old data

---

## Quick Reference

### SQLAlchemy 2.0 Patterns
```python
# Modern column definition
id = mapped_column(Integer, primary_key=True)
name = mapped_column(String(200), nullable=False, index=True)
created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

# Relationship definition
notes = relationship("Note", back_populates="notebook", cascade="all, delete-orphan")
```

### Common Column Types
- `Integer`: IDs, counts, versions
- `String(length)`: Short text, fixed length
- `Text`: Long text, unlimited length  
- `Boolean`: Flags, true/false values
- `DateTime(timezone=True)`: Timestamps
- `JSON`: Flexible data, JSONB in PostgreSQL
- `Float`: Decimal numbers, scores

### Relationship Options
- `back_populates`: Bidirectional relationship
- `cascade="all, delete-orphan"`: Delete children when parent deleted
- `lazy="select"`: Load when accessed (default)
- `order_by`: Sort child collections

---

*This document is the source of truth for SmartNote AI database models. Update it when making model changes.*

*Last Updated: $(date) - Week 1 of Development*