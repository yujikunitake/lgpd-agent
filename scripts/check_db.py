import os
import sys

sys.path.append(os.getcwd())

from sqlalchemy import text

from app.database import engine


def check():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT count(*) FROM document_chunks;"))
        count = res.scalar()
        print(f"Total chunks in database: {count}")


if __name__ == "__main__":
    check()
