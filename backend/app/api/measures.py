"""Measures and Implementation endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, UserRole
from ..models.measure import Measure, MeasureStatus, Implementation
from ..schemas.measure import (
    MeasureCreate, MeasureUpdate, MeasureResponse,
    ImplementationCreate, ImplementationResponse
)
from ..core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/measures", tags=["Measures"])


@router.get("/", response_model=List[MeasureResponse])
def list_measures(
    skip: int = 0,
    limit: int = 100,
    requirement_id: Optional[int] = None,
    status: Optional[MeasureStatus] = None,
    responsible_user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all measures with optional filters."""
    query = db.query(Measure)

    if requirement_id:
        query = query.filter(Measure.requirement_id == requirement_id)

    if status:
        query = query.filter(Measure.status == status)

    if responsible_user_id:
        query = query.filter(Measure.responsible_user_id == responsible_user_id)

    measures = query.order_by(Measure.code).offset(skip).limit(limit).all()
    return measures


@router.get("/my-measures", response_model=List[MeasureResponse])
def list_my_measures(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List measures assigned to current user."""
    measures = db.query(Measure).filter(
        Measure.responsible_user_id == current_user.id
    ).order_by(Measure.code).offset(skip).limit(limit).all()

    return measures


@router.get("/{measure_id}", response_model=MeasureResponse)
def get_measure(
    measure_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific measure by ID."""
    measure = db.query(Measure).filter(Measure.id == measure_id).first()

    if not measure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measure not found"
        )

    return measure


@router.post("/", response_model=MeasureResponse, status_code=status.HTTP_201_CREATED)
def create_measure(
    measure_data: MeasureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.MANAGER))
):
    """Create a new measure (requires MANAGER role)."""
    # Check if code already exists
    existing = db.query(Measure).filter(Measure.code == measure_data.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Measure with code '{measure_data.code}' already exists"
        )

    measure = Measure(**measure_data.model_dump())
    db.add(measure)
    db.commit()
    db.refresh(measure)

    return measure


@router.patch("/{measure_id}", response_model=MeasureResponse)
def update_measure(
    measure_id: int,
    measure_data: MeasureUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a measure. Responsible users can update their measures, managers can update all."""
    measure = db.query(Measure).filter(Measure.id == measure_id).first()

    if not measure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measure not found"
        )

    # Check permissions
    is_responsible = measure.responsible_user_id == current_user.id
    is_manager = current_user.role in [UserRole.ADMIN, UserRole.MANAGER]

    if not is_responsible and not is_manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this measure"
        )

    # Update fields
    update_data = measure_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(measure, field, value)

    db.commit()
    db.refresh(measure)

    return measure


@router.delete("/{measure_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measure(
    measure_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Delete a measure (requires ADMIN role)."""
    measure = db.query(Measure).filter(Measure.id == measure_id).first()

    if not measure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measure not found"
        )

    db.delete(measure)
    db.commit()

    return None


# Implementation endpoints
@router.get("/{measure_id}/implementations", response_model=List[ImplementationResponse])
def list_implementations(
    measure_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all implementation records for a measure."""
    # Check if measure exists
    measure = db.query(Measure).filter(Measure.id == measure_id).first()
    if not measure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measure not found"
        )

    implementations = db.query(Implementation).filter(
        Implementation.measure_id == measure_id
    ).order_by(Implementation.implementation_date.desc()).all()

    return implementations


@router.post("/{measure_id}/implementations", response_model=ImplementationResponse, status_code=status.HTTP_201_CREATED)
def create_implementation(
    measure_id: int,
    implementation_data: ImplementationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new implementation record for a measure."""
    # Check if measure exists
    measure = db.query(Measure).filter(Measure.id == measure_id).first()
    if not measure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measure not found"
        )

    # Verify measure_id matches
    if implementation_data.measure_id != measure_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Measure ID mismatch"
        )

    # Create implementation
    implementation = Implementation(
        **implementation_data.model_dump(),
        implemented_by_id=current_user.id
    )

    db.add(implementation)
    db.commit()
    db.refresh(implementation)

    return implementation
