import logging

from utilities.common.Answer import Answer
from utilities.document_chunking import ChunkingSettings
from utilities.document_loading import LoadingSettings
from utilities.helpers.DocumentChunkingHelper import DocumentChunking
from utilities.helpers.DocumentLoadingHelper import DocumentLoading
from utilities.helpers.DocumentProcessorHelper import Processor
from utilities.helpers.VectorStoreHelper import VectorStoreHelper


def do_internal_chat_learning_tool(question: str) -> str:
    for processor in [
        Processor(document_type="html",
                  chunking=ChunkingSettings({"strategy": "layout", "size": 500, "overlap": 100}),
                  loading=LoadingSettings({"strategy": "chat_learning"}))]:
        try:
            documents = DocumentLoading().load(question, processor.loading)
            documents = DocumentChunking().chunk(documents, processor.chunking)
            keys = list(map(lambda x: x.id, documents))
            documents = [document.convert_to_langchain_document() for document in documents]
            VectorStoreHelper().get_vector_store().add_documents(documents=documents, keys=keys)
        except Exception as e:
            logging.error(f"Error adding embeddings for {question}: {e}")
            raise e

    answer = "Ok, I will remember what you told me!"
    print(f"Answer: {answer}")
    return Answer(question=question,
                  answer=answer,
                  source_documents=[],
                  prompt_tokens=0,
                  completion_tokens=0).to_json()
