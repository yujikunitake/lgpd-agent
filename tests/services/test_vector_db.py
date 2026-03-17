import pytest

from app.schemas.ingestion import DocumentChunk
from app.services.vector_db import PostgresVectorDB


class MockEmbeddingProvider:
    """Mock to simulate OpenAI embedding API without consuming tokens."""
    def get_embedding(self, text: str) -> list[float]:
        # Return a fake 3-dimensional vector for testing
        return [0.1, 0.2, 0.3]


def test_vector_db_implements_rag_protocol():
    """Ensures the class adheres to the RAGProtocol."""
    from app.interfaces.qa_interfaces import RAGProtocol

    embedding_mock = MockEmbeddingProvider()
    db = PostgresVectorDB(connection_string="sqlite:///:memory:", embedding_provider=embedding_mock)
    
    assert isinstance(db, RAGProtocol)


def test_vector_db_retrieves_relevant_chunk():
    """As per Card 6 criteria: query returns at least 1 relevant chunk."""
    embedding_mock = MockEmbeddingProvider()
    
    # We use a fake in-memory db connection string for the unit test
    db = PostgresVectorDB(connection_string="sqlite:///:memory:", embedding_provider=embedding_mock)
    
    # Setup test data
    chunk = DocumentChunk(content="A LGPD protege dados pessoais.", metadata={"Artigo": "1"})
    db.save([chunk])
    
    # Retrieve
    results = db.retrieve("O que a LGPD protege?")
    
    assert len(results) >= 1
    assert "A LGPD protege dados pessoais." in results
