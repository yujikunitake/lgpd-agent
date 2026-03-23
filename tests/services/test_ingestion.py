from app.schemas.ingestion import DocumentChunk
from app.services.ingestion import IngestionService


def test_markdown_chunker_splits_by_headers(ingestion_service):
    mock_markdown = """
    # CAPÍTULO I - DISPOSIÇÕES GERAIS
    Esta é a introdução da lei.

    ## Art. 1º
    Esta Lei dispõe sobre o tratamento de dados pessoais.

    # CAPÍTULO II - DOS DIREITOS DO TITULAR
    ## Art. 18
    O titular dos dados pessoais tem direito a obter do controlador...
    """

    chunks = ingestion_service.split_markdown(mock_markdown)

    # Assert we get a list of DocumentChunk objects
    assert isinstance(chunks, list)
    assert len(chunks) == 3
    assert all(isinstance(c, DocumentChunk) for c in chunks)


def test_markdown_chunker_preserves_header_metadata(ingestion_service):
    mock_markdown = """
    # CAPÍTULO I
    ## Art. 1º
    Texto do artigo 1.
    """
    chunks = ingestion_service.split_markdown(mock_markdown)

    chunk = chunks[0]
    assert chunk.content.strip() == "Texto do artigo 1."

    # Metadata should capture the hierarchy
    assert "CAPÍTULO I" in chunk.metadata.values()
    assert "Art. 1º" in chunk.metadata.values()


def test_split_markdown_by_headers(ingestion_service):
    with open("data/lgpd.md") as f:
        markdown = f.read()

    chunks = ingestion_service.split_markdown(markdown, source="data/lgpd.md")

    # The full law has hundreds of chunks
    assert len(chunks) > 100
    assert chunks[0].metadata["source"] == "data/lgpd.md"


def test_split_markdown_long_article(embeddings_service, vector_store_service):
    # Create a service with a very small chunk size to force recursive splitting
    service = IngestionService(
        embeddings_service=embeddings_service,
        vector_store_service=vector_store_service,
        chunk_size=50,
        chunk_overlap=0,
    )

    long_markdown = """
    ## Art. 1º
    Este é um texto muito longo que deve ser dividido em vários pedaços
    menores pelo RecursiveCharacterTextSplitter.
    """

    chunks = service.split_markdown(long_markdown)

    # has ~100 chars, so it should split into at least 2 chunks of 50 chars.
    assert len(chunks) >= 2
    # All chunks should still have the Article 1 metadata (at Header 2 now)
    assert all(c.metadata["Header 2"] == "Art. 1º" for c in chunks)


def test_ingest_file_saves_to_vector_store(
    ingestion_service, vector_store_service, fake, embeddings_service
):
    # Ingest the real lgpd.md (full law)
    ingestion_service.ingest_file("data/lgpd.md")

    # Use a real embedding from a known sentence in Art 1 to ensure we find it
    target_text = "Esta Lei dispõe sobre o tratamento de dados pessoais"
    target_embedding = embeddings_service.get_embedding(target_text)

    results = vector_store_service.search(target_embedding, top_k=5)

    # Verify that headers were preserved in metadata
    # Art 1 is Header 2 in our new hierarchy
    found = False
    for r in results:
        metadata = r["metadata"]
        # Match "Art. 1" in any header (H1, H2, or H3) to be safe
        # Using "Art. 1" instead of "Art. 1º" to be even more robust
        if any("Art. 1" in str(v) for v in metadata.values()):
            found = True
            break

    assert found, (
        f"Article 1 metadata not found in top results. Results: {[r['metadata'] for r in results]}"
    )
