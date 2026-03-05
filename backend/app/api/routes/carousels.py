from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.carousel import Carousel
from app.schemas.carousel import CarouselCreate, CarouselUpdate, CarouselResponse

router = APIRouter(prefix="/carousels", tags=["carousels"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=CarouselResponse)
def create_carousel(data: CarouselCreate, db: Session = Depends(get_db)):
    carousel = Carousel(**data.model_dump())
    db.add(carousel)
    db.commit()
    db.refresh(carousel)
    return carousel


@router.get("", response_model=list[CarouselResponse])
def list_carousels(db: Session = Depends(get_db)):
    result = db.execute(select(Carousel))
    return list(result.scalars().all())


@router.get("/{carousel_id}", response_model=CarouselResponse)
def get_carousel(carousel_id: UUID, db: Session = Depends(get_db)):
    carousel = db.get(Carousel, carousel_id)
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")
    return carousel


@router.patch("/{carousel_id}", response_model=CarouselResponse)
def update_carousel(carousel_id: UUID, data: CarouselUpdate, db: Session = Depends(get_db)):
    carousel = db.get(Carousel, carousel_id)
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(carousel, key, value)
    db.commit()
    db.refresh(carousel)
    return carousel
