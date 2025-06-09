from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RAGQuery(BaseModel):
    question: str

class UploadedFileBase(BaseModel):
    filename: str

class UploadedFileCreate(UploadedFileBase):
    pass

class UploadedFileUpdate(BaseModel):
    filename: Optional[str] = None

class UploadedFileOut(UploadedFileBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
