#!/usr/bin/env python3
"""
Ingest clinic FAQ JSON into Chroma vector DB.
Uses absolute paths and best practices.
"""

from pathlib import Path
import os

from langchain_community.document_loaders import JSONLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENV_PATH = PROJECT_ROOT / ".env"
DATA_PATH = PROJECT_ROOT / "data" / "clinic_info.json"
DB_PATH = PROJECT_ROOT / "vector_db"

load_dotenv(dotenv_path=ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "clinic_faqs")

embeddings = OpenAIEmbeddings(
    model=OPENAI_EMBEDDING_MODEL,
    openai_api_key=OPENAI_API_KEY,
)

jq_schema = """
to_entries[] | .key as $category | .value[] | {
    text: ("Question: " + .q + "\nAnswer: " + .a),
    metadata: {source: $category, question: .q}
}
"""

loader = JSONLoader(
    file_path=str(DATA_PATH),
    jq_schema=jq_schema,
    text_content=False,
)


def main() -> None:
    print(f"Loading data from: {DATA_PATH}")
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"File not found: {DATA_PATH}")

    print("Parsing JSON with jq schema...")
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")

    texts = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]

    # Delete old collection
    if DB_PATH.exists():
        try:
            client = Chroma(
                persist_directory=str(DB_PATH),
                embedding_function=embeddings,
                collection_name=COLLECTION_NAME,
            )
            client.delete_collection()
            print("Old collection deleted.")
        except Exception as e:
            print(f"Could not delete collection: {e}")

    print("Ingesting into Chroma...")
    Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embeddings,
        persist_directory=str(DB_PATH),
        collection_name=COLLECTION_NAME,
    )
    print("Ingestion complete!")
    print(f"   DB: {DB_PATH}")
    print(f"   Collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()
