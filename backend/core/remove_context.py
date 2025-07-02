import os
import shutil
from core.context_loader import index_pdfs

CHROMA_PATH = "chroma"

def delete_chroma():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    index_pdfs()
    print("Got it")
    return True