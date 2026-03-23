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

    assert len(chunks) == 2
    assert chunks[0].metadata["source"] == "data/lgpd.md"
    assert chunks[1].metadata["source"] == "data/lgpd.md"


def test_split_markdown_long_article(embeddings_service, vector_store_service):
    # Create a service with a very small chunk size to force recursive splitting
    service = IngestionService(
        embeddings_service=embeddings_service,
        vector_store_service=vector_store_service,
        chunk_size=50,
        chunk_overlap=0,
    )

    long_markdown = """
    ### Art. 1º
    Este é um texto muito longo que deve ser dividido em vários pedaços
    menores pelo RecursiveCharacterTextSplitter.
    """

    chunks = service.split_markdown(long_markdown)

    # has ~100 chars, so it should split into at least 2 chunks of 50 chars.
    assert len(chunks) >= 2
    # All chunks should still have the Article 1 metadata
    assert all(c.metadata["Header 3"] == "Art. 1º" for c in chunks)


def test_ingest_file_saves_to_vector_store(ingestion_service, vector_store_service, fake):
    # Ingest the real lgpd.md (2 articles)
    ingestion_service.ingest_file("data/lgpd.md")

    # We should be able to find the content of Art. 1 in the vector store
    # using a simple search for one of the main terms.
    results = vector_store_service.search(fake.vector(), top_k=10)

    # It must have found at least 2 chunks (plus whatever was there before)
    assert len(results) >= 2
    # Verify that headers were preserved in metadata
    assert any("Art. 1º" in str(r["metadata"].values()) for r in results)
