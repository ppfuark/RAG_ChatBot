from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import router
from core.context_loader import index_pdfs

app = FastAPI(title="RAG API com contexto pré-processado")

# ✅ Adiciona o CORS aqui
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

index_pdfs()
app.include_router(router)
