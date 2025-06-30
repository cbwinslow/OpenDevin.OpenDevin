import sys
from types import ModuleType, SimpleNamespace
from pathlib import Path

# Ensure project root is on the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class DummyEmbeddings:
    def __init__(self, *_, **__):
        pass


class DummySplitter:
    def __init__(self, *_, **__):
        pass

    def split_documents(self, docs):
        return docs


class DummyLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        text = Path(self.path).read_text()
        return [SimpleNamespace(page_content=text)]


class DummyStore:
    def __init__(self, *_, **__):
        self.docs = []

    def add_documents(self, docs):
        self.docs.extend(docs)

    def persist(self):
        pass

    def similarity_search(self, text, k=4):
        return self.docs[:k]


# Install stub langchain modules before importing RagBuilder
langchain_embeddings = ModuleType('langchain.embeddings')
langchain_embeddings.HuggingFaceEmbeddings = DummyEmbeddings
langchain_text_splitter = ModuleType('langchain.text_splitter')
langchain_text_splitter.RecursiveCharacterTextSplitter = DummySplitter
langchain_document_loaders = ModuleType('langchain.document_loaders')
langchain_document_loaders.TextLoader = DummyLoader
langchain_vectorstores = ModuleType('langchain.vectorstores')
langchain_chroma = ModuleType('langchain.vectorstores.chroma')
langchain_chroma.Chroma = DummyStore

sys.modules.setdefault('langchain', ModuleType('langchain'))
sys.modules['langchain.embeddings'] = langchain_embeddings
sys.modules['langchain.text_splitter'] = langchain_text_splitter
sys.modules['langchain.document_loaders'] = langchain_document_loaders
sys.modules['langchain.vectorstores'] = langchain_vectorstores
sys.modules['langchain.vectorstores.chroma'] = langchain_chroma


def build_rag(tmp_path):
    from opendevin.rag.builder import RagBuilder

    rb = RagBuilder(persist_dir=str(tmp_path / 'store'))

    f1 = tmp_path / 'one.txt'
    f2 = tmp_path / 'two.txt'
    f1.write_text('alpha beta gamma')
    f2.write_text('delta epsilon zeta')

    rb.index_files([f1, f2])
    return rb


def test_index_files(tmp_path):
    rb = build_rag(tmp_path)
    assert len(rb.store.docs) == 2


def test_query(tmp_path):
    rb = build_rag(tmp_path)
    results = rb.query('alpha', k=1)
    assert results == ['alpha beta gamma']
