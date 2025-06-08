from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from core.context_loader import index_pdfs
from core.db import SessionLocal
from models.models import UploadedFile

router = APIRouter()
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def post_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        db = SessionLocal()
        file_record = UploadedFile(filename=file.filename)
        db.add(file_record)
        db.commit()
        db.close()

        try:
            index_pdfs()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
    
    return {"filename": file.filename}