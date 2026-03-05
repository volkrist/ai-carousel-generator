from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.carousel import Carousel
from app.models.design import DesignSettings
from app.schemas.design import DesignUpdate, DesignResponse

router = APIRouter(prefix="/carousels", tags=["design"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{carousel_id}/design", response_model=DesignResponse)
def get_design(carousel_id: UUID, db: Session = Depends(get_db)):
    carousel = db.get(Carousel, carousel_id)
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    design = db.get(DesignSettings, carousel_id)
    if not design:
        design = DesignSettings(carousel_id=carousel_id)
        db.add(design)
        db.commit()
        db.refresh(design)

    return design


@router.patch("/{carousel_id}/design", response_model=DesignResponse)
def update_design(
    carousel_id: UUID, payload: DesignUpdate, db: Session = Depends(get_db)
):
    carousel = db.get(Carousel, carousel_id)
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    design = db.get(DesignSettings, carousel_id)
    if not design:
        design = DesignSettings(carousel_id=carousel_id)
        db.add(design)
        db.commit()
        db.refresh(design)

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(design, k, v)

    db.commit()
    db.refresh(design)
    return design
