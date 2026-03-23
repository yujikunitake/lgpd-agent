import json

from sqlalchemy import text

from app.database import engine


def check():
    with engine.connect() as conn:
        # Note: SQLAlchemy uses metadata_ to avoid conflict with Base.metadata
        res = conn.execute(text("SELECT content, metadata_ FROM document_chunks LIMIT 5;"))
        rows = res.fetchall()
        print("Sample of 5 chunks found in DB:")
        for row in rows:
            content = row[0][:100].replace("\n", " ").strip()
            metadata = row[1]
            print("---")
            print(f"Content: {content}...")
            print(f"Metadata: {json.dumps(metadata, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    check()
