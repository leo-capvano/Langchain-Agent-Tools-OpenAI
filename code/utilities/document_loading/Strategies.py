from enum import Enum


class LoadingStrategy(Enum):
    LAYOUT = 'layout'
    READ = 'read'
    WEB = 'web'
    DOCX = 'docx'
    LOCAL_PDF = 'local_pdf'
    CHAT_LEARNING = 'chat_learning'


def get_document_loader(loader_strategy: str):
    if loader_strategy == LoadingStrategy.LOCAL_PDF.value:
        from .LocalPdfDocumentLoader import LocalPdfDocumentLoading
        return LocalPdfDocumentLoading()
    elif loader_strategy == LoadingStrategy.CHAT_LEARNING.value:
        from .TextDocumentLoader import TextDocumentLoading
        return TextDocumentLoading()
    else:
        raise Exception(f"Unknown loader strategy: {loader_strategy}")
