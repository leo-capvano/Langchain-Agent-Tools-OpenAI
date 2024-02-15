import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class EnvHelper:
    def __init__(self, **kwargs) -> None:
        load_dotenv()
        # Azure OpenAI
        self.AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY', '')
        # Orchestration Settings
        self.ORCHESTRATION_STRATEGY = os.getenv('ORCHESTRATION_STRATEGY', 'langchain')
        # rag strategy (pgvector, azure_search)
        self.RAG_STRATEGY = os.getenv('RAG_STRATEGY', 'pgvector')
        # local postgres vectorstore
        self.PG_USER = os.getenv('PG_USER', 'postgres_usr')
        self.PG_PWD = os.getenv('PG_PWD', 'postgres_pwd')
        self.PG_DB = os.getenv('PG_DB', 'postgres_db')
        self.PG_PORT = os.getenv('PG_PORT', '5433')
        self.PG_ENDPOINT = os.getenv('PG_ENDPOINT', '127.0.0.1')
        self.PG_DEFAULT_RAG_COLLECTION_NAME = os.getenv('PG_DEFAULT_RAG_COLLECTION_NAME', 'chatbot_knowledge')
