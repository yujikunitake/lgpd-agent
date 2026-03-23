from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from app.interfaces.qa_interfaces import EmbeddingsProtocol
from app.schemas.ingestion import DocumentChunk
from app.services.vector_store import VectorStoreService


class IngestionService:
    """Service responsible for loading and chunking markdown documents."""

    def __init__(
        self,
        embeddings_service: EmbeddingsProtocol,
        vector_store_service: VectorStoreService,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
    ):
        """Initializes the service and its dependencies.

        Args:
            embeddings_service (EmbeddingsProtocol): Service to generate embeddings.
            vector_store_service (VectorStoreService): Service to handle vector search.
            chunk_size (int): Max size of a text chunk.
            chunk_overlap (int): Overlap between recursive chunks.
        """
        self.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on,
            strip_headers=True,
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.embeddings_service = embeddings_service
        self.vector_store_service = vector_store_service

    def ingest_file(self, file_path: str) -> None:
        """Processes a file, generates embeddings, and saves to the vector store.

        Args:
            file_path (str): The path to the markdown file to ingest.
        """
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        chunks = self.split_markdown(content, source=file_path)

        for chunk in chunks:
            embedding = self.embeddings_service.get_embedding(chunk.content)
            self.vector_store_service.add_chunk(chunk.content, embedding, chunk.metadata)

    def split_markdown(self, markdown_text: str, source: str | None = None) -> list[DocumentChunk]:
        """Splits markdown text into DocumentChunks preserving header metadata.

        Args:
            markdown_text (str): The markdown content to split.
            source (str | None): Optional source identifier.

        Returns:
            list[DocumentChunk]: A list of chunks with content and metadata.
        """
        header_docs = self.header_splitter.split_text(markdown_text)

        final_chunks = []
        recursive_docs = self.text_splitter.split_documents(header_docs)

        for doc in recursive_docs:
            metadata = doc.metadata.copy()
            if source:
                metadata["source"] = source
            final_chunks.append(DocumentChunk(content=doc.page_content, metadata=metadata))

        return final_chunks
