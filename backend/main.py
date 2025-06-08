from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import router
from core.context_loader import index_pdfs
from models.models import Base
from core.db import engine


app = FastAPI(title="RAG API with data uploadable")

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

Base.metadata.create_all(bind=engine)
index_pdfs()

app.include_router(router)
