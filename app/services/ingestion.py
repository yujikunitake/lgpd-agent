from langchain_text_splitters import MarkdownHeaderTextSplitter

from app.schemas.ingestion import DocumentChunk


class IngestionService:
    """Service responsible for loading and chunking markdown documents."""

    def __init__(self):
        """Initializes the service and configures the markdown text splitter.

        The splitter is configured to track specific markdown headers so that
        hierarchical context is preserved in the resulting chunks.
        """
        # We define which Markdown headers we care about for the LLM context.
        # This preserves Chapter and Article hierarchies.
        self.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on,
            strip_headers=True,  # Strip the headers from the content since they are in metadata
        )

    def chunk_markdown(self, markdown_text: str) -> list[DocumentChunk]:
        """Splits markdown text into DocumentChunks preserving header metadata."""
        return [
            DocumentChunk(content=doc.page_content, metadata=doc.metadata)
            for doc in self.markdown_splitter.split_text(markdown_text)
        ]
