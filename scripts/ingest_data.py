import os
import sys

from app.database import engine, init_db
from app.services.embeddings import EmbeddingsService
from app.services.ingestion import IngestionService
from app.services.vector_store import VectorStoreService


def main():
    print("Starting LGPD Data Ingestion...")

    # 1. Initialize DB (Extension + Tables)
    init_db()

    # 2. Setup Services
    embeddings_service = EmbeddingsService()
    vector_store_service = VectorStoreService(engine)
    ingestion_service = IngestionService(embeddings_service, vector_store_service)

    # 3. Define source file
    source_file = "data/lgpd.md"

    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' not found.")
        sys.exit(1)

    # 4. Ingest
    print(f"Processing {source_file}...")
    ingestion_service.ingest_file(source_file)

    print("Ingestion complete! The database is now populated with LGPD content.")


if __name__ == "__main__":
    main()
