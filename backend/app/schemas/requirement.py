"""Requirement schemas."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from ..models.requirement import RequirementCategory


class RequirementBase(BaseModel):
    """Base requirement schema."""
    code: str = Field(..., max_length=50)
    category: RequirementCategory
    title: str = Field(..., max_length=500)
    description: str
    legal_reference: Optional[str] = Field(None, max_length=255)
    iso27001_controls: Optional[str] = None
    is_mandatory: bool = True
    priority: int = Field(1, ge=1, le=5)
    implementation_guidance: Optional[str] = None
    evidence_required: Optional[str] = None


class RequirementCreate(RequirementBase):
    """Schema for creating a requirement."""
    pass


class RequirementUpdate(BaseModel):
    """Schema for updating a requirement."""
    category: Optional[RequirementCategory] = None
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    legal_reference: Optional[str] = Field(None, max_length=255)
    iso27001_controls: Optional[str] = None
    is_mandatory: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    implementation_guidance: Optional[str] = None
    evidence_required: Optional[str] = None


class RequirementResponse(RequirementBase):
    """Requirement response schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
