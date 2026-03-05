from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.slide import Slide
from app.schemas.slide import SlideResponse, SlideUpdate

router = APIRouter(prefix="/carousels", tags=["slides"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{carousel_id}/slides", response_model=list[SlideResponse])
def get_slides(carousel_id: UUID, db: Session = Depends(get_db)):
    result = db.execute(
        select(Slide).where(Slide.carousel_id == carousel_id).order_by(Slide.order)
    )
    return list(result.scalars().all())


@router.patch("/{carousel_id}/slides/{slide_id}", response_model=SlideResponse)
def update_slide(
    carousel_id: UUID,
    slide_id: UUID,
    data: SlideUpdate,
    db: Session = Depends(get_db),
):
    slide = db.execute(
        select(Slide).where(
            Slide.id == slide_id,
            Slide.carousel_id == carousel_id,
        )
    ).scalar_one_or_none()

    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(slide, key, value)

    db.commit()
    db.refresh(slide)

    return slide
