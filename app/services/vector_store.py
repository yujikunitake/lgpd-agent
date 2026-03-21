from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class VectorStoreService:
    """Service to handle vector operations in PostgreSQL using pgvector."""

    def __init__(self, engine):
        """Initializes the VectorStoreService with a SQLAlchemy engine.

        Args:
            engine: The SQLAlchemy engine used to connect to the database.
        """
        self.engine = engine

    def add_chunk(self, content: str, embedding: list[float], metadata: dict[str, Any]) -> None:
        """Saves a single text chunk with its embedding to the database.

        Args:
            content (str): The text content of the chunk.
            embedding (list[float]): The 384-dimensional vector embedding.
            metadata (dict[str, Any]): Additional metadata for the chunk.
        """
        with Session(self.engine) as session:
            chunk = DocumentChunk(content=content, embedding=embedding, metadata_=metadata)
            session.add(chunk)
            session.commit()

    def search(self, query_vector: list[float], top_k: int = 5) -> list[dict[str, Any]]:
        """Searches for the most similar chunks using Euclidean distance (L2).

        Args:
            query_vector (list[float]): The vector to search for.
            top_k (int): The number of top results to return. Defaults to 5.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing content and metadata.
        """
        with Session(self.engine) as session:
            query = (
                select(DocumentChunk)
                .order_by(DocumentChunk.embedding.l2_distance(query_vector))
                .limit(top_k)
            )

            results = session.execute(query).scalars().all()

            return [{"content": r.content, "metadata": r.metadata_} for r in results]
