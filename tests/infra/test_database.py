from sqlalchemy import text

from app.database import engine, init_db


def test_database_connection():
    """Test if we can connect to the database and execute a simple query."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_pgvector_extension_exists():
    """Test if the pgvector extension is available and enabled."""
    init_db()
    with engine.connect() as conn:
        # Check if 'vector' is in the list of installed extensions
        result = conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
        extension = result.scalar()
        assert extension == "vector"
