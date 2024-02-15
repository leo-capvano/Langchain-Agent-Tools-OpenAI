import os

from langchain_community.vectorstores.pgvector import PGVector

from .EnvHelper import EnvHelper
from .LLMHelper import LLMHelper


class VectorStoreHelper:
    def __init__(self):
        pass

    def get_vector_store(self):
        llm_helper = LLMHelper()
        env_helper = EnvHelper()
        if env_helper.RAG_STRATEGY == "pgvector":
            pg_connection_string = PGVector.connection_string_from_db_params(
                driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
                host=os.environ.get("PGVECTOR_HOST", env_helper.PG_ENDPOINT),
                port=int(os.environ.get("PGVECTOR_PORT", env_helper.PG_PORT)),
                database=os.environ.get("PGVECTOR_DATABASE", env_helper.PG_DB),
                user=os.environ.get("PGVECTOR_USER", env_helper.PG_USER),
                password=os.environ.get("PGVECTOR_PASSWORD", env_helper.PG_PWD),
            )
            return PGVector(collection_name=env_helper.PG_DEFAULT_RAG_COLLECTION_NAME,
                            connection_string=pg_connection_string,
                            embedding_function=llm_helper.get_embedding_model())
