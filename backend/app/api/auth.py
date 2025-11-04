"""Authentication endpoints."""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, AuthProvider
from ..schemas.user import LoginRequest, Token, UserResponse
from ..core.security import verify_password, create_access_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with username and password.
    Returns JWT access token.
    """
    # Find user
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password (only for local users)
    if user.auth_provider != AuthProvider.LOCAL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User is authenticated via {user.auth_provider}. Please use the appropriate login method."
        )

    if not user.hashed_password or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/entra/login")
def entra_login():
    """
    Initiate Microsoft Entra (Azure AD) OAuth flow.
    This endpoint redirects to Microsoft login page.
    """
    if not settings.ENTRA_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Microsoft Entra authentication is not enabled"
        )

    # TODO: Implement MSAL OAuth flow
    # For now, return instructions
    return {
        "message": "Microsoft Entra authentication endpoint",
        "status": "not_yet_implemented",
        "instructions": [
            "1. Configure ENTRA_* variables in .env",
            "2. Set ENTRA_ENABLED=True",
            "3. Implement MSAL OAuth flow",
            "4. See docs/ENTRA_SETUP.md for details"
        ]
    }


@router.get("/entra/callback")
def entra_callback(code: Optional[str] = None, error: Optional[str] = None):
    """
    Microsoft Entra OAuth callback endpoint.
    Handles the redirect after user authenticates with Microsoft.
    """
    if not settings.ENTRA_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Microsoft Entra authentication is not enabled"
        )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication error: {error}"
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No authorization code received"
        )

    # TODO: Implement MSAL token exchange and user creation/login
    return {
        "message": "Microsoft Entra callback endpoint",
        "status": "not_yet_implemented",
        "code": code
    }
