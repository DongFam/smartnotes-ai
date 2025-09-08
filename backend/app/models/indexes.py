# Performance indexes for SmartNote AI models
# These indexes should be created via Alembic migrations

"""
SQL commands for creating performance indexes.
Run these via Alembic migrations for optimal database performance.

Usage in migration:
    from alembic import op
    
    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_username', 'users', ['username'], unique=True)
    # ... etc
"""

# Primary indexes for User model
USER_INDEXES = [
    # Already exists: email unique index
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username);", 
    "CREATE INDEX IF NOT EXISTS idx_users_subscription_tier ON users(subscription_tier);",
    "CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);",
]

# Primary indexes for Notebook model  
NOTEBOOK_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_notebooks_user_id ON notebooks(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_notebooks_is_archived ON notebooks(is_archived) WHERE is_archived = false;",
    "CREATE INDEX IF NOT EXISTS idx_notebooks_is_favorite ON notebooks(is_favorite) WHERE is_favorite = true;",
    # Composite indexes for common queries
    "CREATE INDEX IF NOT EXISTS idx_notebooks_user_active ON notebooks(user_id, is_archived);",
    "CREATE INDEX IF NOT EXISTS idx_notebooks_user_favorite ON notebooks(user_id, is_favorite) WHERE is_favorite = true;",
]

# Primary indexes for Note model
NOTE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_notes_notebook_id ON notes(notebook_id);",
    "CREATE INDEX IF NOT EXISTS idx_notes_is_archived ON notes(is_archived) WHERE is_archived = false;", 
    "CREATE INDEX IF NOT EXISTS idx_notes_enhancement_version ON notes(enhancement_version);",
    "CREATE INDEX IF NOT EXISTS idx_notes_enhancement_status ON notes(enhancement_status);",
    # Composite indexes for filtered queries
    "CREATE INDEX IF NOT EXISTS idx_notes_notebook_active ON notes(notebook_id, is_archived);",
    "CREATE INDEX IF NOT EXISTS idx_notes_notebook_enhanced ON notes(notebook_id, is_enhanced);",
    # Full-text search on title and content
    "CREATE INDEX IF NOT EXISTS idx_notes_title_search ON notes USING gin(to_tsvector('english', title));",
    "CREATE INDEX IF NOT EXISTS idx_notes_content_search ON notes USING gin(to_tsvector('english', coalesce(content, '')));",
]

# Primary indexes for Enhancement model
ENHANCEMENT_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_enhancements_note_id ON enhancements(note_id);",
    "CREATE INDEX IF NOT EXISTS idx_enhancements_version ON enhancements(version);", 
    "CREATE INDEX IF NOT EXISTS idx_enhancements_is_current ON enhancements(is_current) WHERE is_current = true;",
    "CREATE INDEX IF NOT EXISTS idx_enhancements_status ON enhancements(status) WHERE status != 'completed';",
    "CREATE INDEX IF NOT EXISTS idx_enhancements_type ON enhancements(enhancement_type);",
    # Composite indexes for version tracking
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_enhancements_note_version ON enhancements(note_id, version);",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_enhancements_note_current ON enhancements(note_id) WHERE is_current = true;",
    # Processing queue queries
    "CREATE INDEX IF NOT EXISTS idx_enhancements_processing_queue ON enhancements(status, created_at) WHERE status IN ('pending', 'processing');",
]

# All indexes combined
ALL_INDEXES = USER_INDEXES + NOTEBOOK_INDEXES + NOTE_INDEXES + ENHANCEMENT_INDEXES

def get_index_creation_sql():
    """Returns SQL statements for creating all performance indexes."""
    return ALL_INDEXES

def get_index_drop_sql():
    """Returns SQL statements for dropping all performance indexes."""
    drop_statements = []
    for create_sql in ALL_INDEXES:
        # Extract index name from CREATE INDEX statement
        if "CREATE UNIQUE INDEX" in create_sql:
            index_name = create_sql.split("CREATE UNIQUE INDEX IF NOT EXISTS ")[1].split(" ON ")[0]
        elif "CREATE INDEX" in create_sql:
            index_name = create_sql.split("CREATE INDEX IF NOT EXISTS ")[1].split(" ON ")[0]
        else:
            continue
        drop_statements.append(f"DROP INDEX IF EXISTS {index_name};")
    
    return drop_statements

# Index usage examples for common queries
QUERY_EXAMPLES = """
-- Find user's active notebooks (uses idx_notebooks_user_active)
SELECT * FROM notebooks 
WHERE user_id = ? AND is_archived = false
ORDER BY updated_at DESC;

-- Find notebook's active notes (uses idx_notes_notebook_active) 
SELECT * FROM notes
WHERE notebook_id = ? AND is_archived = false
ORDER BY updated_at DESC;

-- Get current enhancement for note (uses idx_enhancements_note_current)
SELECT * FROM enhancements
WHERE note_id = ? AND is_current = true;

-- Get enhancement history (uses idx_enhancements_note_version)
SELECT * FROM enhancements
WHERE note_id = ?
ORDER BY version;

-- Search notes by content (uses idx_notes_content_search)
SELECT * FROM notes
WHERE to_tsvector('english', coalesce(content, '')) @@ plainto_tsquery('english', ?);

-- Find pending enhancements (uses idx_enhancements_processing_queue)
SELECT * FROM enhancements  
WHERE status = 'pending'
ORDER BY created_at;
"""