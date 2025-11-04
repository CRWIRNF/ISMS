"""User schemas."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from ..models.user import UserRole, AuthProvider


class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    """User schema as stored in database."""
    id: int
    auth_provider: AuthProvider
    entra_id: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    role: UserRole
    auth_provider: AuthProvider
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT token payload data."""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str
