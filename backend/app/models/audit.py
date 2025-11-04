"""Audit log model for compliance tracking."""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from ..database import Base


class AuditAction(str, enum.Enum):
    """Audit action types."""
    # User actions
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"

    # Requirement actions
    REQUIREMENT_CREATED = "requirement_created"
    REQUIREMENT_UPDATED = "requirement_updated"
    REQUIREMENT_DELETED = "requirement_deleted"

    # Measure actions
    MEASURE_CREATED = "measure_created"
    MEASURE_UPDATED = "measure_updated"
    MEASURE_DELETED = "measure_deleted"
    MEASURE_STATUS_CHANGED = "measure_status_changed"

    # Risk actions
    RISK_CREATED = "risk_created"
    RISK_UPDATED = "risk_updated"
    RISK_DELETED = "risk_deleted"
    RISK_ASSESSED = "risk_assessed"

    # Incident actions
    INCIDENT_CREATED = "incident_created"
    INCIDENT_UPDATED = "incident_updated"
    INCIDENT_REPORTED = "incident_reported"
    INCIDENT_CLOSED = "incident_closed"

    # Document actions
    DOCUMENT_CREATED = "document_created"
    DOCUMENT_UPDATED = "document_updated"
    DOCUMENT_DELETED = "document_deleted"
    DOCUMENT_APPROVED = "document_approved"

    # System actions
    SYSTEM_CONFIG_CHANGED = "system_config_changed"
    BACKUP_CREATED = "backup_created"
    BACKUP_RESTORED = "backup_restored"


class AuditLog(Base):
    """Audit log for tracking all system changes."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Action details
    action = Column(Enum(AuditAction), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False)  # e.g., "User", "Measure", "Risk"
    entity_id = Column(Integer, nullable=True)

    # User who performed the action
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    username = Column(String(100), nullable=True)  # Denormalized for deleted users

    # Details
    description = Column(Text, nullable=False)
    old_value = Column(Text, nullable=True)  # JSON
    new_value = Column(Text, nullable=True)  # JSON

    # Request metadata
    ip_address = Column(String(45), nullable=True)  # IPv6 max length
    user_agent = Column(String(500), nullable=True)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        """String representation."""
        return f"<AuditLog(action='{self.action}', entity='{self.entity_type}', user='{self.username}')>"
