"""Document model for policies, procedures, and evidence."""

import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Date
from ..database import Base


class DocumentType(str, enum.Enum):
    """Document types."""
    POLICY = "policy"  # Richtlinie
    PROCEDURE = "procedure"  # Verfahrensanweisung
    GUIDELINE = "guideline"  # Leitfaden
    TEMPLATE = "template"  # Vorlage
    EVIDENCE = "evidence"  # Nachweis
    REPORT = "report"  # Bericht
    CERTIFICATE = "certificate"  # Zertifikat
    OTHER = "other"


class Document(Base):
    """Document model."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    # Identification
    title = Column(String(500), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Links
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    measure_id = Column(Integer, ForeignKey("measures.id"), nullable=True)

    # File information
    file_path = Column(String(1000), nullable=True)
    file_name = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)  # in bytes
    mime_type = Column(String(100), nullable=True)

    # Content (for text-based documents stored in DB)
    content = Column(Text, nullable=True)

    # Version control
    version = Column(String(50), nullable=True)

    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Review
    review_date = Column(Date, nullable=True)
    next_review_date = Column(Date, nullable=True)
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approval_date = Column(Date, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation."""
        return f"<Document(id={self.id}, title='{self.title}', type='{self.document_type}')>"
