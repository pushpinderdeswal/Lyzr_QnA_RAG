from pathlib import Path
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DB_PATH = PROJECT_ROOT / "vector_db"


load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "clinic_faqs")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

embeddings = OpenAIEmbeddings(
    model=OPENAI_EMBEDDING_MODEL, openai_api_key=os.getenv("OPENAI_API_KEY")
)


def get_retriever(k: int = 2):
    """
    Returns a Chroma retriever with k results.
    """
    vectorstore = Chroma(
        persist_directory=str(DB_PATH),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )
    return vectorstore.as_retriever(search_kwargs={"k": k})
