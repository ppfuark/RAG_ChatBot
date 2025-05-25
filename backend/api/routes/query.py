from fastapi import APIRouter
from pydantic import BaseModel
from core.rag import query_rag

router = APIRouter()

class QueryInput(BaseModel):
    question: str

@router.post("/query")
def query_docs(input: QueryInput):
    response = query_rag(input.question)
    return {"answer": response}
