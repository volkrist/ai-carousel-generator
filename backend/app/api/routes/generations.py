from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.carousel import Carousel
from app.models.generation import Generation
from app.models.slide import Slide
from app.schemas.generation import GenerationCreate, GenerationResponse
from app.services.llm_service import generate_slides

router = APIRouter(prefix="/generations", tags=["generations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_generation(generation_id: UUID) -> None:
    db = SessionLocal()
    gen = None
    try:
        gen = db.get(Generation, generation_id)
        if not gen:
            return

        carousel = db.get(Carousel, gen.carousel_id)
        if not carousel:
            gen.status = "failed"
            gen.error = "Carousel not found"
            gen.finished_at = datetime.utcnow()
            db.commit()
            return

        gen.status = "running"
        db.commit()

        source_text = ""
        if carousel.source_payload and isinstance(carousel.source_payload, dict):
            source_text = (
                carousel.source_payload.get("text")
                or carousel.source_payload.get("url")
                or ""
            )
        if not source_text:
            gen.status = "failed"
            gen.error = "Empty source_text in carousel.source_payload"
            gen.finished_at = datetime.utcnow()
            db.commit()
            return

        result = generate_slides(
            source_text=source_text,
            language=carousel.lang or "ru",
            slides_count=carousel.slides_count or 8,
            style_hint=carousel.style_hint,
            model="gpt-4o-mini",
        )

        # удалить старые слайды (re-generate)
        db.execute(delete(Slide).where(Slide.carousel_id == carousel.id))
        db.commit()

        for s in result.slides:
            db.add(
                Slide(
                    carousel_id=carousel.id,
                    order=s.order,
                    title=s.title,
                    body=s.body,
                    footer=s.footer,
                )
            )

        gen.status = "done"
        gen.result_json = result.model_dump()
        gen.finished_at = datetime.utcnow()
        carousel.status = "ready"
        db.commit()

    except Exception as e:
        if db.is_active:
            gen = db.get(Generation, generation_id)
            if gen:
                gen.status = "failed"
                gen.error = str(e)
                gen.finished_at = datetime.utcnow()
                db.commit()
    finally:
        db.close()


@router.post("", response_model=GenerationResponse)
def create_generation(
    payload: GenerationCreate,
    bg: BackgroundTasks,
    db: Session = Depends(get_db),
):
    carousel = db.get(Carousel, payload.carousel_id)
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    carousel.status = "generating"
    gen = Generation(carousel_id=payload.carousel_id, status="queued")
    db.add(gen)
    db.commit()
    db.refresh(gen)

    bg.add_task(run_generation, gen.id)

    return gen


@router.get("/{generation_id}", response_model=GenerationResponse)
def get_generation(generation_id: UUID, db: Session = Depends(get_db)):
    gen = db.get(Generation, generation_id)
    if not gen:
        raise HTTPException(status_code=404, detail="Generation not found")
    return gen
