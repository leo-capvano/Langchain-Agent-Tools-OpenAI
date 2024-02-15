import logging
import sys
from typing import List

from utilities.common.SourceDocument import SourceDocument
from utilities.helpers.DocumentChunkingHelper import DocumentChunking, ChunkingSettings
from utilities.helpers.DocumentLoadingHelper import DocumentLoading, LoadingSettings
from utilities.helpers.DocumentProcessorHelper import Processor
from utilities.helpers.VectorStoreHelper import VectorStoreHelper

if __name__ == '__main__':
    # source_url = "../data/Benefit_Options.pdf"
    file_path = sys.argv[1]

    vector_store_helper = VectorStoreHelper()
    vector_store = vector_store_helper.get_vector_store()
    for processor in [
        Processor(document_type="html", chunking=ChunkingSettings({"strategy": "layout", "size": 500, "overlap": 100}),
                  loading=LoadingSettings({"strategy": "local_pdf"}))]:
        try:
            document_loading = DocumentLoading()
            document_chunking = DocumentChunking()
            documents: List[SourceDocument] = []
            documents = document_loading.load(file_path, processor.loading)
            documents = document_chunking.chunk(documents, processor.chunking)
            keys = list(map(lambda x: x.id, documents))
            documents = [document.convert_to_langchain_document() for document in documents]
            vector_store.add_documents(documents=documents, keys=keys)
        except Exception as e:
            logging.error(f"Error adding embeddings for {file_path}: {e}")
            raise e
