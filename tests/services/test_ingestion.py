from app.schemas.ingestion import DocumentChunk
from app.services.ingestion import IngestionService


def test_markdown_chunker_splits_by_headers():
    mock_markdown = """
    # CAPÍTULO I - DISPOSIÇÕES GERAIS
    Esta é a introdução da lei.

    ## Art. 1º
    Esta Lei dispõe sobre o tratamento de dados pessoais.

    # CAPÍTULO II - DOS DIREITOS DO TITULAR
    ## Art. 18
    O titular dos dados pessoais tem direito a obter do controlador...
    """

    service = IngestionService()
    chunks = service.chunk_markdown(mock_markdown)

    # Assert we get a list of DocumentChunk objects
    assert isinstance(chunks, list)
    assert len(chunks) == 3
    assert all(isinstance(c, DocumentChunk) for c in chunks)


def test_markdown_chunker_preserves_header_metadata():
    mock_markdown = """
    # CAPÍTULO I
    ## Art. 1º
    Texto do artigo 1.
    """
    service = IngestionService()
    chunks = service.chunk_markdown(mock_markdown)

    chunk = chunks[0]
    assert chunk.content.strip() == "Texto do artigo 1."

    # Metadata should capture the hierarchy
    assert "CAPÍTULO I" in chunk.metadata.values()
    assert "Art. 1º" in chunk.metadata.values()
