from langchain_text_splitters import MarkdownHeaderTextSplitter

from app.schemas.ingestion import DocumentChunk


class IngestionService:
    def __init__(self):
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
        # Langchain does the heavy lifting of parsing markdown
        langchain_docs = self.markdown_splitter.split_text(markdown_text)

        chunks = []
        for doc in langchain_docs:
            chunks.append(DocumentChunk(content=doc.page_content, metadata=doc.metadata))

        return chunks
