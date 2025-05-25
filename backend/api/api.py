from fastapi import FastAPI
from api.routes import upload, query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir conexão com o front-end React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(query.router, prefix="/api")
