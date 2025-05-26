from fastapi import APIRouter
from schemas.rag_schema import RAGQuery
from core.rag import query_rag

router = APIRouter()

@router.post("/ask")
def ask_question(data: RAGQuery):
    resposta = query_rag(data.question)
    return {"answer": resposta}
