"""Incident schemas."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from ..models.incident import IncidentSeverity, IncidentStatus


class IncidentBase(BaseModel):
    """Base incident schema."""
    incident_id: str = Field(..., max_length=50)
    title: str = Field(..., max_length=500)
    description: str
    severity: IncidentSeverity
    category: Optional[str] = Field(None, max_length=100)
    affected_systems: Optional[str] = None
    affected_data: Optional[str] = None
    estimated_impact: Optional[str] = None
    requires_external_reporting: bool = False


class IncidentCreate(IncidentBase):
    """Schema for creating an incident."""
    detected_at: datetime


class IncidentUpdate(BaseModel):
    """Schema for updating an incident."""
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    severity: Optional[IncidentSeverity] = None
    status: Optional[IncidentStatus] = None
    category: Optional[str] = Field(None, max_length=100)
    affected_systems: Optional[str] = None
    affected_data: Optional[str] = None
    estimated_impact: Optional[str] = None
    response_actions: Optional[str] = None
    root_cause: Optional[str] = None
    lessons_learned: Optional[str] = None
    reported_at: Optional[datetime] = None
    contained_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    reported_to_authorities: Optional[bool] = None
    authority_report_date: Optional[datetime] = None
    authority_reference: Optional[str] = Field(None, max_length=255)
    assigned_to_id: Optional[int] = None


class IncidentResponse(IncidentBase):
    """Incident response schema."""
    id: int
    status: IncidentStatus
    response_actions: Optional[str]
    root_cause: Optional[str]
    lessons_learned: Optional[str]
    detected_at: datetime
    reported_at: Optional[datetime]
    contained_at: Optional[datetime]
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    reported_to_authorities: bool
    authority_report_date: Optional[datetime]
    authority_reference: Optional[str]
    reported_by_id: int
    assigned_to_id: Optional[int]
    related_requirement_id: Optional[int]
    related_risk_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
