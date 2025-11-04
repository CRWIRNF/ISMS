"""Incident management models."""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean
from ..database import Base


class IncidentSeverity(str, enum.Enum):
    """Incident severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentStatus(str, enum.Enum):
    """Incident status."""
    NEW = "new"
    REPORTED = "reported"  # Reported to authorities
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Incident(Base):
    """Security incident model."""

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    # Identification
    incident_id = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "INC-2024-001"
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)

    # Classification
    severity = Column(Enum(IncidentSeverity), nullable=False, index=True)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.NEW, nullable=False, index=True)
    category = Column(String(100), nullable=True)  # e.g., "Malware", "Data Breach", "DDoS"

    # Impact
    affected_systems = Column(Text, nullable=True)
    affected_data = Column(Text, nullable=True)
    estimated_impact = Column(Text, nullable=True)

    # Detection and Response
    detected_at = Column(DateTime, nullable=False)
    reported_at = Column(DateTime, nullable=True)
    contained_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    # NIS2 Reporting (24-hour requirement)
    requires_external_reporting = Column(Boolean, default=False, nullable=False)
    reported_to_authorities = Column(Boolean, default=False, nullable=False)
    authority_report_date = Column(DateTime, nullable=True)
    authority_reference = Column(String(255), nullable=True)

    # Response
    response_actions = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    lessons_learned = Column(Text, nullable=True)

    # Ownership
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Links
    related_requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    related_risk_id = Column(Integer, ForeignKey("risks.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation."""
        return f"<Incident(incident_id='{self.incident_id}', severity='{self.severity}', status='{self.status}')>"
