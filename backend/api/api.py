from api.routes import upload, query
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(upload.router, prefix="/api")
api_router.include_router(query.router, prefix="/api")
