"""Main FastAPI application."""

import json
import os
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db, SessionLocal
from .models.user import User, UserRole, AuthProvider
from .models.requirement import Requirement
from .core.security import get_password_hash
from .api import auth, users, requirements, measures, risks

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="NIS2 Compliance Management System - Information Security Management System",
    debug=settings.DEBUG,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(requirements.router, prefix="/api")
app.include_router(measures.router, prefix="/api")
app.include_router(risks.router, prefix="/api/risks", tags=["risks"])


@app.on_event("startup")
def startup_event():
    """Initialize database and load initial data."""
    # Create tables
    init_db()

    # Create admin user if not exists
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not admin_user:
            admin_user = User(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                full_name="System Administrator",
                role=UserRole.ADMIN,
                auth_provider=AuthProvider.LOCAL,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                is_active=True,
                is_verified=True,
            )
            db.add(admin_user)
            db.commit()
            print(f"✅ Created admin user: {settings.ADMIN_USERNAME}")
        else:
            print(f"ℹ️  Admin user already exists: {settings.ADMIN_USERNAME}")

        # Load NIS2 requirements if not already loaded
        req_count = db.query(Requirement).count()
        if req_count == 0:
            load_nis2_requirements(db)
        else:
            print(f"ℹ️  NIS2 requirements already loaded ({req_count} requirements)")

    finally:
        db.close()


def load_nis2_requirements(db):
    """Load NIS2 requirements from JSON file."""
    data_file = Path(__file__).parent / "data" / "nis2_requirements.json"

    if not data_file.exists():
        print(f"⚠️  NIS2 requirements file not found: {data_file}")
        return

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        requirements = data.get("requirements", [])
        for req_data in requirements:
            requirement = Requirement(**req_data)
            db.add(requirement)

        db.commit()
        print(f"✅ Loaded {len(requirements)} NIS2 requirements")

    except Exception as e:
        print(f"❌ Error loading NIS2 requirements: {e}")
        db.rollback()


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "NIS2 ISMS API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
