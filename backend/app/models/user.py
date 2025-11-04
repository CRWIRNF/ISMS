"""User model."""

import enum
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
from ..database import Base


class UserRole(str, enum.Enum):
    """User roles."""
    ADMIN = "admin"
    MANAGER = "manager"
    AUDITOR = "auditor"
    USER = "user"


class AuthProvider(str, enum.Enum):
    """Authentication provider."""
    LOCAL = "local"
    ENTRA = "entra"  # Microsoft Entra (Azure AD)


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Nullable for Entra users
    full_name = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    auth_provider = Column(Enum(AuthProvider), default=AuthProvider.LOCAL, nullable=False)

    # Entra (Azure AD) specific fields
    entra_id = Column(String(255), unique=True, nullable=True, index=True)
    entra_tenant_id = Column(String(255), nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        """String representation."""
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
