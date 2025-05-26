from fastapi import FastAPI
from api.v1.api import router
from core.context_loader import index_pdfs

app = FastAPI(title="RAG API com contexto pré-processado")

index_pdfs()

app.include_router(router)