import pytest
from app.services.vector_store import VectorStoreService

from app.database import Base, engine


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_search_similar_chunks(fake):
    store = VectorStoreService(engine)

    content = "Artigo 1: Esta Lei dispõe sobre a proteção de dados pessoais."
    embedding = [fake.pyfloat()] * 384
    metadata = {"source": "artigo_1.txt"}

    store.add_chunk(content, embedding, metadata)
    results = store.search(embedding, top_k=1)

    assert len(results) == 1
    assert results[0]["content"] == content
    assert results[0]["metadata"] == metadata
