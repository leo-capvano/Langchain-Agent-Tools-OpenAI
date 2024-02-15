import re
from typing import List

from langchain_core.documents import Document

from .DocumentLoadingBase import DocumentLoadingBase
from ..common.SourceDocument import SourceDocument


def clean_up_document_page_content(documents):
    for document in documents:
        document.page_content = re.sub('\n{3,}', '\n\n', document.page_content)
        # Remove half non-ascii character from start/end of doc content
        pattern = re.compile(
            r"[\x00-\x1f\x7f\u0080-\u00a0\u2000-\u3000\ufff0-\uffff]"
        )
        document.page_content = re.sub(pattern, "", document.page_content)
        if document.page_content == "":
            documents.remove(document)


class TextDocumentLoading(DocumentLoadingBase):
    def __init__(self) -> None:
        super().__init__()

    def load(self, text: str) -> List[SourceDocument]:
        text_document = Document(page_content=text, metadata={'source': 'coming from chat runtime learning'})
        documents = [text_document]
        clean_up_document_page_content(documents)
        source_documents: List[SourceDocument] = [
            SourceDocument(
                content=document.page_content,
                source=document.metadata['source'],
            )
            for document in documents
        ]
        return source_documents
