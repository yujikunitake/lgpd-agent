import pytest

from app.database import Base, engine


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_search_similar_chunks(fake, vector_store_service):
    content = "Artigo 1: Esta Lei dispõe sobre a proteção de dados pessoais."
    embedding = fake.vector(dims=384)
    metadata = {"source": "artigo_1.txt"}

    vector_store_service.add_chunk(content, embedding, metadata)
    results = vector_store_service.search(embedding, top_k=1)

    assert len(results) == 1
    assert results[0]["content"] == content
    assert results[0]["metadata"] == metadata
