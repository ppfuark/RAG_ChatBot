from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os

from core.db import SessionLocal
from models.models import UploadedFile
from core.context_loader import index_pdfs
from schemas.schemas import UploadedFileCreate, UploadedFileUpdate, UploadedFileOut

router = APIRouter()
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/", response_model=UploadedFileOut)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File saving failed: {e}")

    try:
        file_record = UploadedFile(filename=file.filename)
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    try:
        index_pdfs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")

    return file_record

# READ
@router.get("/", response_model=List[UploadedFileOut])
def list_files(db: Session = Depends(get_db)):
    return db.query(UploadedFile).all()

# READ
@router.get("/{file_id}", response_model=UploadedFileOut)
def get_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

# UPDATE
@router.put("/{file_id}", response_model=UploadedFileOut)
def update_file(file_id: int, file_data: UploadedFileUpdate, db: Session = Depends(get_db)):
    file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file_data.filename:
        old_path = os.path.join(UPLOAD_DIR, file.filename)
        new_path = os.path.join(UPLOAD_DIR, file_data.filename)

        try:
            os.rename(old_path, new_path)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Original file not found on disk")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File rename failed: {e}")

        file.filename = file_data.filename

    db.commit()
    db.refresh(file)
    return file

# DELETE
@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File deletion failed: {e}")

    db.delete(file)
    db.commit()
    return {"detail": "File deleted successfully"}
