from fastapi import APIRouter
from api.v1.routes import rag_routes, file_routes

router = APIRouter()
router.include_router(rag_routes.router, prefix="/rag", tags=["RAG"])
router.include_router(file_routes.router, prefix="/file", tags=["FILE"])