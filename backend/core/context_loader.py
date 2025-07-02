import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from core.embedding import get_embedding_function

CHROMA_PATH = "chroma"
DATA_PATH = "data"

# NEW FUNCTION: Load a single PDF file
def load_single_pdf(file_path: str) -> list[Document]:
    loader = PyPDFLoader(file_path)
    return loader.load()

# SPLIT DOCUMENTS
def split_documents(documents: list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=20,
        length_function=len
    )
    return splitter.split_documents(documents)

# ADD UNIQUE IDS
def calculate_chunk_ids(chunks: list[Document]):
    last_page_id = None
    current_chunk_index = 0
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
        current_chunk_index = current_chunk_index + 1 if current_page_id == last_page_id else 0
        chunk.metadata["id"] = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
    return chunks

# ADD TO CHROMA DB
def add_to_chroma(chunks: list[Document]):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    chunks = calculate_chunk_ids(chunks)
    existing = set(db.get(include=[])["ids"])
    new_chunks = [chunk for chunk in chunks if chunk.metadata["id"] not in existing]
    if new_chunks:
        db.add_documents(new_chunks, ids=[c.metadata["id"] for c in new_chunks])

# NEW FUNCTION: index a single file
def index_pdf(file_path: str):
    try:
        documents = load_single_pdf(file_path)
        chunks = split_documents(documents)
        add_to_chroma(chunks)
    except Exception as e:
        print(f"[index_pdf ERRO] {e}")
        raise

# NEW FUNCTION: index all files
def index_pdfs():
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

def load_documents():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    return loader.load()