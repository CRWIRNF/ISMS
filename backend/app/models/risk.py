"""Risk management models."""

import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Date, Float
from ..database import Base


class RiskLevel(str, enum.Enum):
    """Risk level classification."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class RiskStatus(str, enum.Enum):
    """Risk status."""
    IDENTIFIED = "identified"
    ASSESSED = "assessed"
    TREATED = "treated"
    ACCEPTED = "accepted"
    MONITORED = "monitored"
    CLOSED = "closed"


class Risk(Base):
    """Risk model for risk management."""

    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)

    # Identification
    risk_id = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "RISK-2024-001"
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)

    # Classification
    category = Column(String(100), nullable=True)  # e.g., "Cyber Security", "Data Protection"

    # Risk Assessment
    likelihood = Column(Integer, nullable=False)  # 1-5 scale
    impact = Column(Integer, nullable=False)  # 1-5 scale
    risk_score = Column(Float, nullable=False)  # likelihood * impact
    risk_level = Column(Enum(RiskLevel), nullable=False, index=True)

    # Treatment
    status = Column(Enum(RiskStatus), default=RiskStatus.IDENTIFIED, nullable=False, index=True)
    treatment_plan = Column(Text, nullable=True)

    # Residual Risk (after treatment)
    residual_likelihood = Column(Integer, nullable=True)
    residual_impact = Column(Integer, nullable=True)
    residual_risk_score = Column(Float, nullable=True)
    residual_risk_level = Column(Enum(RiskLevel), nullable=True)

    # Links
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    related_measure_id = Column(Integer, ForeignKey("measures.id"), nullable=True)

    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timeline
    identified_date = Column(Date, nullable=False)
    target_closure_date = Column(Date, nullable=True)
    actual_closure_date = Column(Date, nullable=True)

    # Review
    last_review_date = Column(Date, nullable=True)
    next_review_date = Column(Date, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation."""
        return f"<Risk(risk_id='{self.risk_id}', level='{self.risk_level}', status='{self.status}')>"
