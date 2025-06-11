from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from typing import List
from core.context_loader import index_pdf

router = APIRouter()
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def post_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        try:
            index_pdf(file_path)
        except Exception as e:
            print(f"Erro no index_pdf: {e}")
            raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
    
    return {"filename": file.filename}

@router.get("/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename)

@router.get("/", response_model=List[str])
async def list_files():
    return os.listdir(UPLOAD_DIR)

@router.delete("/{filename}")
async def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(file_path)
    return {"detail": f"File '{filename}' deleted successfully."}