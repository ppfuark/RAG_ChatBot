from fastapi import APIRouter
from api.v1.routes import rag_routes

router = APIRouter()
router.include_router(rag_routes.router, prefix="/rag", tags=["RAG"])