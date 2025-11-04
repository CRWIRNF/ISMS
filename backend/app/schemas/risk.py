"""Risk schemas."""

from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, Field
from ..models.risk import RiskLevel, RiskStatus


class RiskBase(BaseModel):
    """Base risk schema."""
    risk_id: str = Field(..., max_length=50)
    title: str = Field(..., max_length=500)
    description: str
    category: Optional[str] = Field(None, max_length=100)
    likelihood: int = Field(..., ge=1, le=5)
    impact: int = Field(..., ge=1, le=5)
    treatment_plan: Optional[str] = None
    requirement_id: Optional[int] = None
    related_measure_id: Optional[int] = None


class RiskCreate(RiskBase):
    """Schema for creating a risk."""
    identified_date: date


class RiskUpdate(BaseModel):
    """Schema for updating a risk."""
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    likelihood: Optional[int] = Field(None, ge=1, le=5)
    impact: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[RiskStatus] = None
    treatment_plan: Optional[str] = None
    residual_likelihood: Optional[int] = Field(None, ge=1, le=5)
    residual_impact: Optional[int] = Field(None, ge=1, le=5)
    target_closure_date: Optional[date] = None
    actual_closure_date: Optional[date] = None
    last_review_date: Optional[date] = None
    next_review_date: Optional[date] = None


class RiskResponse(RiskBase):
    """Risk response schema."""
    id: int
    risk_score: float
    risk_level: RiskLevel
    status: RiskStatus
    residual_likelihood: Optional[int]
    residual_impact: Optional[int]
    residual_risk_score: Optional[float]
    residual_risk_level: Optional[RiskLevel]
    owner_id: int
    identified_date: date
    target_closure_date: Optional[date]
    actual_closure_date: Optional[date]
    last_review_date: Optional[date]
    next_review_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
