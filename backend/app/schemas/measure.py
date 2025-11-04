"""Measure and Implementation schemas."""

from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, Field
from ..models.measure import MeasureStatus


class MeasureBase(BaseModel):
    """Base measure schema."""
    requirement_id: int
    code: str = Field(..., max_length=50)
    title: str = Field(..., max_length=500)
    description: str
    status: MeasureStatus = MeasureStatus.NOT_STARTED
    implementation_details: Optional[str] = None
    responsible_user_id: Optional[int] = None
    planned_start_date: Optional[date] = None
    planned_completion_date: Optional[date] = None
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class MeasureCreate(MeasureBase):
    """Schema for creating a measure."""
    pass


class MeasureUpdate(BaseModel):
    """Schema for updating a measure."""
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    status: Optional[MeasureStatus] = None
    implementation_details: Optional[str] = None
    responsible_user_id: Optional[int] = None
    planned_start_date: Optional[date] = None
    planned_completion_date: Optional[date] = None
    actual_completion_date: Optional[date] = None
    last_review_date: Optional[date] = None
    next_review_date: Optional[date] = None
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class MeasureResponse(MeasureBase):
    """Measure response schema."""
    id: int
    actual_completion_date: Optional[date]
    last_review_date: Optional[date]
    next_review_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ImplementationBase(BaseModel):
    """Base implementation schema."""
    measure_id: int
    title: str = Field(..., max_length=500)
    description: str
    implementation_date: date
    evidence_location: Optional[str] = Field(None, max_length=500)


class ImplementationCreate(ImplementationBase):
    """Schema for creating an implementation."""
    pass


class ImplementationResponse(ImplementationBase):
    """Implementation response schema."""
    id: int
    implemented_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
