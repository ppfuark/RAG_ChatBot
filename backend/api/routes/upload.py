from fastapi import APIRouter, UploadFile, File
import os
from core.indexer import index_pdfs

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join("data", file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    index_pdfs()
    return {"message": f"{file.filename} uploaded and indexed successfully"}
