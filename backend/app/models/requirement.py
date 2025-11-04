"""NIS2 Requirement models."""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from ..database import Base


class RequirementCategory(str, enum.Enum):
    """NIS2 Requirement categories based on Article 21."""
    RISK_MANAGEMENT = "risk_management"  # Risikoanalyse und Sicherheitskonzepte
    INCIDENT_MANAGEMENT = "incident_management"  # Bewältigung von Sicherheitsvorfällen
    BUSINESS_CONTINUITY = "business_continuity"  # Aufrechterhaltung des Betriebs
    SUPPLY_CHAIN = "supply_chain"  # Lieferkettensicherheit
    SECURITY_ACQUISITION = "security_acquisition"  # Sicherheit bei Erwerb, Entwicklung und Wartung
    EFFECTIVENESS_TESTING = "effectiveness_testing"  # Prüfung und Bewertung der Wirksamkeit
    CYBER_HYGIENE = "cyber_hygiene"  # Cyberhygiene und Schulungen
    CRYPTOGRAPHY = "cryptography"  # Verschlüsselung und Kryptografie
    PERSONNEL_SECURITY = "personnel_security"  # Personalsicherheit
    MFA_COMMUNICATION = "mfa_communication"  # Multi-Faktor-Authentifizierung


class Requirement(Base):
    """NIS2 Requirement model."""

    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)

    # Identification
    code = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "NIS2-A21-01"
    category = Column(Enum(RequirementCategory), nullable=False, index=True)

    # Content
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    legal_reference = Column(String(255), nullable=True)  # e.g., "Artikel 21 Abs. 2 lit. a"

    # ISO 27001 Mapping
    iso27001_controls = Column(Text, nullable=True)  # JSON array of ISO control IDs

    # Priority and Status
    is_mandatory = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=1, nullable=False)  # 1=highest, 5=lowest

    # Guidance
    implementation_guidance = Column(Text, nullable=True)
    evidence_required = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation."""
        return f"<Requirement(code='{self.code}', category='{self.category}')>"
