"""Risk Management API endpoints."""

from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_, and_, func

from ..database import get_db
from ..models.risk import Risk, RiskLevel, RiskStatus
from ..schemas.risk import RiskCreate, RiskUpdate, RiskResponse
from ..core.dependencies import get_current_user
from ..models.user import User


router = APIRouter()


def calculate_risk_score(likelihood: int, impact: int) -> float:
    """Calculate risk score from likelihood and impact."""
    return float(likelihood * impact)


def determine_risk_level(risk_score: float) -> RiskLevel:
    """Determine risk level based on risk score."""
    if risk_score >= 20:
        return RiskLevel.CRITICAL
    elif risk_score >= 15:
        return RiskLevel.HIGH
    elif risk_score >= 10:
        return RiskLevel.MEDIUM
    elif risk_score >= 5:
        return RiskLevel.LOW
    else:
        return RiskLevel.NEGLIGIBLE


@router.post("/", response_model=RiskResponse, status_code=201)
def create_risk(
    risk_data: RiskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new risk."""

    # Check if risk_id already exists
    existing_risk = db.query(Risk).filter(Risk.risk_id == risk_data.risk_id).first()
    if existing_risk:
        raise HTTPException(status_code=400, detail="Risk ID already exists")

    # Calculate risk score and level
    risk_score = calculate_risk_score(risk_data.likelihood, risk_data.impact)
    risk_level = determine_risk_level(risk_score)

    # Create new risk
    db_risk = Risk(
        **risk_data.model_dump(),
        risk_score=risk_score,
        risk_level=risk_level,
        owner_id=current_user.id,
        status=RiskStatus.IDENTIFIED
    )

    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)

    return db_risk


@router.get("/", response_model=List[RiskResponse])
def get_risks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[RiskStatus] = None,
    level: Optional[RiskLevel] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|risk_score|identified_date|risk_id)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all risks with filtering and pagination."""

    query = db.query(Risk)

    # Apply filters
    if status:
        query = query.filter(Risk.status == status)

    if level:
        query = query.filter(Risk.risk_level == level)

    if category:
        query = query.filter(Risk.category == category)

    if search:
        search_filter = or_(
            Risk.risk_id.ilike(f"%{search}%"),
            Risk.title.ilike(f"%{search}%"),
            Risk.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Apply sorting
    sort_column = getattr(Risk, sort_by)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # Apply pagination
    risks = query.offset(skip).limit(limit).all()

    return risks


@router.get("/statistics")
def get_risk_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get risk statistics for dashboard."""

    total_risks = db.query(Risk).count()

    # Count by status
    status_counts = {}
    for status in RiskStatus:
        count = db.query(Risk).filter(Risk.status == status).count()
        status_counts[status.value] = count

    # Count by level
    level_counts = {}
    for level in RiskLevel:
        count = db.query(Risk).filter(Risk.risk_level == level).count()
        level_counts[level.value] = count

    # Average risk score
    avg_risk_score = db.query(func.avg(Risk.risk_score)).scalar() or 0.0

    # High priority risks (Critical and High)
    high_priority_count = db.query(Risk).filter(
        and_(
            Risk.risk_level.in_([RiskLevel.CRITICAL, RiskLevel.HIGH]),
            Risk.status.in_([RiskStatus.IDENTIFIED, RiskStatus.ASSESSED])
        )
    ).count()

    # Overdue risks (past target_closure_date and not closed)
    today = date.today()
    overdue_count = db.query(Risk).filter(
        and_(
            Risk.target_closure_date < today,
            Risk.status != RiskStatus.CLOSED,
            Risk.status != RiskStatus.ACCEPTED
        )
    ).count()

    # Risks requiring review
    review_required = db.query(Risk).filter(
        and_(
            Risk.next_review_date <= today,
            Risk.status.in_([RiskStatus.TREATED, RiskStatus.MONITORED])
        )
    ).count()

    return {
        "total_risks": total_risks,
        "status_distribution": status_counts,
        "level_distribution": level_counts,
        "average_risk_score": round(avg_risk_score, 2),
        "high_priority_risks": high_priority_count,
        "overdue_risks": overdue_count,
        "review_required": review_required
    }


@router.get("/matrix")
def get_risk_matrix(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get risk matrix data (likelihood vs impact distribution)."""

    matrix = {}

    for likelihood in range(1, 6):
        for impact in range(1, 6):
            count = db.query(Risk).filter(
                and_(
                    Risk.likelihood == likelihood,
                    Risk.impact == impact,
                    Risk.status != RiskStatus.CLOSED
                )
            ).count()

            matrix[f"{likelihood}_{impact}"] = count

    return {"matrix": matrix}


@router.get("/categories")
def get_risk_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of all risk categories."""

    categories = db.query(Risk.category).distinct().filter(Risk.category.isnot(None)).all()

    return {"categories": [cat[0] for cat in categories if cat[0]]}


@router.get("/{risk_id}", response_model=RiskResponse)
def get_risk(
    risk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific risk by ID."""

    risk = db.query(Risk).filter(Risk.id == risk_id).first()

    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")

    return risk


@router.put("/{risk_id}", response_model=RiskResponse)
def update_risk(
    risk_id: int,
    risk_update: RiskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a risk."""

    risk = db.query(Risk).filter(Risk.id == risk_id).first()

    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")

    # Update fields
    update_data = risk_update.model_dump(exclude_unset=True)

    # Recalculate risk score if likelihood or impact changed
    if "likelihood" in update_data or "impact" in update_data:
        new_likelihood = update_data.get("likelihood", risk.likelihood)
        new_impact = update_data.get("impact", risk.impact)
        update_data["risk_score"] = calculate_risk_score(new_likelihood, new_impact)
        update_data["risk_level"] = determine_risk_level(update_data["risk_score"])

    # Calculate residual risk if provided
    if "residual_likelihood" in update_data and "residual_impact" in update_data:
        if update_data["residual_likelihood"] and update_data["residual_impact"]:
            update_data["residual_risk_score"] = calculate_risk_score(
                update_data["residual_likelihood"],
                update_data["residual_impact"]
            )
            update_data["residual_risk_level"] = determine_risk_level(
                update_data["residual_risk_score"]
            )

    for key, value in update_data.items():
        setattr(risk, key, value)

    db.commit()
    db.refresh(risk)

    return risk


@router.delete("/{risk_id}", status_code=204)
def delete_risk(
    risk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a risk."""

    risk = db.query(Risk).filter(Risk.id == risk_id).first()

    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")

    # Check if user is admin or risk owner
    if not current_user.is_superuser and risk.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this risk")

    db.delete(risk)
    db.commit()

    return None


@router.post("/{risk_id}/accept", response_model=RiskResponse)
def accept_risk(
    risk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accept a risk (risk acceptance decision)."""

    risk = db.query(Risk).filter(Risk.id == risk_id).first()

    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")

    risk.status = RiskStatus.ACCEPTED
    risk.actual_closure_date = date.today()

    db.commit()
    db.refresh(risk)

    return risk


@router.post("/{risk_id}/close", response_model=RiskResponse)
def close_risk(
    risk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Close a risk."""

    risk = db.query(Risk).filter(Risk.id == risk_id).first()

    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")

    risk.status = RiskStatus.CLOSED
    risk.actual_closure_date = date.today()

    db.commit()
    db.refresh(risk)

    return risk
