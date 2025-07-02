import sqlite3
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from typing import List
from core.context_loader import index_pdf, index_pdfs
from core.remove_context import delete_chroma

router = APIRouter()
CHROMA_DB_PATH = "chroma/chroma.sqlite3"
CHROMA_DIR = "chroma"
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
    
    try:
        # First delete the file
        os.remove(file_path)
        
        # Then handle Chroma cleanup
        try:
            # Safely delete the Chroma DB
            if not safe_delete_chroma_db():
                print("Chroma DB file didn't exist - skipping deletion")
            
            # Rebuild the index
            index_pdfs()
            
            return {"detail": f"File '{filename}' deleted and Chroma index rebuilt."}
            
        except Exception as chroma_error:
            # If Chroma deletion failed, try to continue with index rebuild
            try:
                index_pdfs()
                return {
                    "detail": f"File '{filename}' deleted but Chroma cleanup failed. Index rebuilt.",
                    "warning": str(chroma_error)
                }
            except Exception as rebuild_error:
                raise HTTPException(
                    status_code=500,
                    detail=f"File deleted but both Chroma cleanup and index rebuild failed: {str(chroma_error)} | {str(rebuild_error)}"
                )
                
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete file: {str(e)}"
        )
    

def safe_delete_chroma_db():
    """Safely delete the Chroma database with proper connection handling"""
    max_retries = 3
    retry_delay = 0.5  # seconds
    
    for attempt in range(max_retries):
        try:
            # Close any existing SQLite connections
            try:
                conn = sqlite3.connect(CHROMA_DB_PATH)
                conn.close()
            except:
                pass
            
            # Delete the database file
            if os.path.exists(CHROMA_DB_PATH):
                os.remove(CHROMA_DB_PATH)
                return True
            
            # If we got here, the file didn't exist
            return False
            
        except PermissionError as pe:
            if attempt == max_retries - 1:
                raise
            time.sleep(retry_delay)
        except Exception as e:
            raise