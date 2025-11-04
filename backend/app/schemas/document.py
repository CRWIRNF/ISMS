"""Document schemas."""

from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, Field
from ..models.document import DocumentType


class DocumentBase(BaseModel):
    """Base document schema."""
    title: str = Field(..., max_length=500)
    document_type: DocumentType
    description: Optional[str] = None
    requirement_id: Optional[int] = None
    measure_id: Optional[int] = None
    content: Optional[str] = None
    version: Optional[str] = Field(None, max_length=50)


class DocumentCreate(DocumentBase):
    """Schema for creating a document."""
    pass


class DocumentUpdate(BaseModel):
    """Schema for updating a document."""
    title: Optional[str] = Field(None, max_length=500)
    document_type: Optional[DocumentType] = None
    description: Optional[str] = None
    content: Optional[str] = None
    version: Optional[str] = Field(None, max_length=50)
    review_date: Optional[date] = None
    next_review_date: Optional[date] = None


class DocumentResponse(DocumentBase):
    """Document response schema."""
    id: int
    file_path: Optional[str]
    file_name: Optional[str]
    file_size: Optional[int]
    mime_type: Optional[str]
    owner_id: int
    created_by_id: int
    review_date: Optional[date]
    next_review_date: Optional[date]
    approved_by_id: Optional[int]
    approval_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
