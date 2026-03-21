from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Column, Integer, String

from app.database import Base


class DocumentChunk(Base):
    """SQLAlchemy model for storing LGPD text chunks and their embeddings."""

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    metadata_ = Column(JSON, nullable=False)
    embedding = Column(Vector(384), nullable=False)
