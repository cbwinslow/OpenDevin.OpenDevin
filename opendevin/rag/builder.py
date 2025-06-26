"""Simple RAG database builder using LangChain and Chroma."""

from pathlib import Path
from typing import Iterable

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores.chroma import Chroma


class RagBuilder:
    """Utility to create and query a simple RAG database."""

    def __init__(self, persist_dir: str = './rag_store') -> None:
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings()
        self.store = Chroma(persist_directory=self.persist_dir,
                            embedding_function=self.embeddings)

    def index_files(self, paths: Iterable[Path]) -> None:
        docs = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        for path in paths:
            loader = TextLoader(str(path))
            docs.extend(splitter.split_documents(loader.load()))
        self.store.add_documents(docs)
        self.store.persist()

    def query(self, text: str, k: int = 4) -> list[str]:
        """Return top `k` similar documents."""
        results = self.store.similarity_search(text, k=k)
        return [r.page_content for r in results]
