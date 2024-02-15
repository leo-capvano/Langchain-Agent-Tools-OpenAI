import logging

from utilities.helpers.DocumentChunkingHelper import DocumentChunking, ChunkingSettings
from utilities.helpers.DocumentLoadingHelper import DocumentLoading, LoadingSettings
from utilities.helpers.DocumentProcessorHelper import Processor
from utilities.helpers.VectorStoreHelper import VectorStoreHelper


class ChatLearningProcessorHelper:

    @staticmethod
    def add_knowledge(text_to_learn: str):

        vector_store_helper = VectorStoreHelper()
        vector_store = vector_store_helper.get_vector_store()
        for processor in [
            Processor(document_type="html",
                      chunking=ChunkingSettings({"strategy": "layout", "size": 500, "overlap": 100}),
                      loading=LoadingSettings({"strategy": "chat_learning"}))]:
            try:
                document_loading = DocumentLoading()
                document_chunking = DocumentChunking()
                documents = document_loading.load(text_to_learn, processor.loading)
                documents = document_chunking.chunk(documents, processor.chunking)
                keys = list(map(lambda x: x.id, documents))
                documents = [document.convert_to_langchain_document() for document in documents]
                vector_store.add_documents(documents=documents, keys=keys)
            except Exception as e:
                logging.error(f"Error adding embeddings for {text_to_learn}: {e}")
                raise e
