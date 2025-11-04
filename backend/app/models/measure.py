"""Measure and Implementation models."""

import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from ..database import Base


class MeasureStatus(str, enum.Enum):
    """Status of measure implementation."""
    NOT_STARTED = "not_started"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    NOT_APPLICABLE = "not_applicable"


class Measure(Base):
    """Measure to fulfill NIS2 requirements."""

    __tablename__ = "measures"

    id = Column(Integer, primary_key=True, index=True)

    # Link to requirement
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)

    # Identification
    code = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "M-001"
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)

    # Implementation details
    status = Column(Enum(MeasureStatus), default=MeasureStatus.NOT_STARTED, nullable=False, index=True)
    implementation_details = Column(Text, nullable=True)

    # Responsibility
    responsible_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Timeline
    planned_start_date = Column(Date, nullable=True)
    planned_completion_date = Column(Date, nullable=True)
    actual_completion_date = Column(Date, nullable=True)

    # Review
    last_review_date = Column(Date, nullable=True)
    next_review_date = Column(Date, nullable=True)

    # Effectiveness
    effectiveness_score = Column(Float, nullable=True)  # 0.0 - 1.0

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation."""
        return f"<Measure(code='{self.code}', status='{self.status}')>"


class Implementation(Base):
    """Implementation tracking for measures."""

    __tablename__ = "implementations"

    id = Column(Integer, primary_key=True, index=True)

    # Link to measure
    measure_id = Column(Integer, ForeignKey("measures.id"), nullable=False)

    # Implementation entry
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)

    # Who did what when
    implemented_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    implementation_date = Column(Date, nullable=False)

    # Evidence
    evidence_location = Column(String(500), nullable=True)  # File path or URL

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation."""
        return f"<Implementation(measure_id={self.measure_id}, date={self.implementation_date})>"
