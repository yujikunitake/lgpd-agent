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


def test_search_returns_closest_match(fake, vector_store_service):
    content = "Artigo 1: Esta Lei dispõe sobre a proteção de dados pessoais."
    target_vector = fake.vector(dims=384)
    metadata = {"source": "artigo_1.txt"}

    vector_store_service.add_chunk(content, target_vector, metadata)

    for _ in range(5):
        vector_store_service.add_chunk(
            fake.paragraph(), fake.vector(), {"source": fake.file_name()}
        )

    results = vector_store_service.search(target_vector, top_k=1)

    assert results[0]["content"] == content
    assert results[0]["metadata"] == metadata
