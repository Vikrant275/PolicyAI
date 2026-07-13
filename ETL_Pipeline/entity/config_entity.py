# config.py
# from pydantic_settings import BaseSettings
from typing import Literal,List


class Settings:
    # Extraction
    pdf_extractor: Literal["pdfplumber", "unstructured", "hybrid"] = "hybrid"
    pdf_documents_path: str = 'D:\\PolicyAI\\documents'
    text_elem_file_path :str = 'D:\\PolicyAI\\artifact\\text_element.pkl'
    from_page = 3

    # Chunking
    chunk_size: int = 1024  # tokens, not characters
    chunk_overlap: int = 200
    separators: List[str] = ['\n\n','\n','.',' ']
    chunks_file_path: str = 'D:\\PolicyAI\\artifact\\chunks.pkl'

    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"
    embedded_vec_file_path = 'D:\\PolicyAI\\artifact\\embedded.npy'
    vector_size: int = 384  # for OpenAI batching
    # embedding_cache_ttl: int = 86400  # 24h

    # Vector DB
    vector_db_type: Literal["qdrant"] = "qdrant"
    path_of_db: str ="D:\\PolicyAI\\DATA_DB"
    index_name: str = "prod-rag-index"
    collection_name: str = "prod-rag-collection"
    distance: str = "Cosine"
    hybrid_search_alpha: float = 0.7  # weight for dense vs sparse

    # LLM
    llm_model: str = "gemma4:4b"
    generation_temperature: float = 0.3
    max_tokens: int = 2048

    # Async / Retries
    max_retries: int = 3
    retry_backoff: float = 2.0

    class Config:
        env_file = ".env.prod"


# settings = Settings()