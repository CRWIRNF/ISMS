"""NIS2 Requirements endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, UserRole
from ..models.requirement import Requirement, RequirementCategory
from ..schemas.requirement import RequirementCreate, RequirementUpdate, RequirementResponse
from ..core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/requirements", tags=["Requirements"])


@router.get("/", response_model=List[RequirementResponse])
def list_requirements(
    skip: int = 0,
    limit: int = 100,
    category: Optional[RequirementCategory] = None,
    is_mandatory: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all NIS2 requirements with optional filters."""
    query = db.query(Requirement)

    if category:
        query = query.filter(Requirement.category == category)

    if is_mandatory is not None:
        query = query.filter(Requirement.is_mandatory == is_mandatory)

    requirements = query.order_by(Requirement.priority, Requirement.code).offset(skip).limit(limit).all()
    return requirements


@router.get("/categories", response_model=List[str])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all requirement categories."""
    return [category.value for category in RequirementCategory]


@router.get("/{requirement_id}", response_model=RequirementResponse)
def get_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific requirement by ID."""
    requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()

    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )

    return requirement


@router.post("/", response_model=RequirementResponse, status_code=status.HTTP_201_CREATED)
def create_requirement(
    requirement_data: RequirementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.MANAGER))
):
    """Create a new requirement (requires MANAGER role)."""
    # Check if code already exists
    existing = db.query(Requirement).filter(Requirement.code == requirement_data.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requirement with code '{requirement_data.code}' already exists"
        )

    requirement = Requirement(**requirement_data.model_dump())
    db.add(requirement)
    db.commit()
    db.refresh(requirement)

    return requirement


@router.patch("/{requirement_id}", response_model=RequirementResponse)
def update_requirement(
    requirement_id: int,
    requirement_data: RequirementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.MANAGER))
):
    """Update a requirement (requires MANAGER role)."""
    requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()

    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )

    # Update fields
    update_data = requirement_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(requirement, field, value)

    db.commit()
    db.refresh(requirement)

    return requirement


@router.delete("/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Delete a requirement (requires ADMIN role)."""
    requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()

    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )

    db.delete(requirement)
    db.commit()

    return None
