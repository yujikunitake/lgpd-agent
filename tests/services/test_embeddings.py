from app.services.embeddings import EmbeddingsService


def test_generate_embedding_returns_correct_vector_size():
    embeddings = EmbeddingsService()
    vector = embeddings.get_embedding("LGPD é a lei de proteção de dados")

    assert isinstance(vector, list)
    assert len(vector) == 384
    assert all(isinstance(x, float) for x in vector)
