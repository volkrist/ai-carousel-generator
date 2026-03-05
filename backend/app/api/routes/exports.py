from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.carousel import Carousel
from app.models.design import DesignSettings
from app.models.export import Export
from app.models.slide import Slide
from app.services.export_service import export_carousel_to_zip, upload_export_zip
from app.services.storage_service import get_file_url

router = APIRouter(prefix="/exports", tags=["exports"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_export(export_id: UUID) -> None:
    db = SessionLocal()
    try:
        exp = db.get(Export, export_id)
        if not exp:
            return

        carousel = db.get(Carousel, exp.carousel_id)
        if not carousel:
            exp.status = "failed"
            exp.error = "Carousel not found"
            exp.finished_at = datetime.utcnow()
            db.commit()
            return

        exp.status = "running"
        db.commit()

        slides = db.execute(
            select(Slide).where(Slide.carousel_id == carousel.id).order_by(Slide.order)
        ).scalars().all()

        if not slides:
            exp.status = "failed"
            exp.error = "No slides to export"
            exp.finished_at = datetime.utcnow()
            db.commit()
            return

        design = db.get(DesignSettings, carousel.id)
        if not design:
            design_dict = {}
        else:
            design_dict = {
                c.name: getattr(design, c.name) for c in design.__table__.columns
            }

        slides_dicts = [
            {"order": s.order, "title": s.title, "body": s.body, "footer": s.footer}
            for s in slides
        ]

        zip_bytes = export_carousel_to_zip(slides_dicts, design_dict)
        uploaded = upload_export_zip(zip_bytes)

        exp.status = "done"
        exp.zip_asset_key = uploaded["key"]
        exp.finished_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        if db.is_active:
            try:
                exp = db.get(Export, export_id)
                if exp:
                    exp.status = "failed"
                    exp.error = str(e)
                    exp.finished_at = datetime.utcnow()
                    db.commit()
            except Exception:
                db.rollback()
    finally:
        db.close()


@router.post("")
def create_export(body: dict, bg: BackgroundTasks, db: Session = Depends(get_db)):
    carousel_id = body.get("carousel_id")
    if not carousel_id:
        raise HTTPException(status_code=422, detail="carousel_id is required")

    try:
        cid = UUID(str(carousel_id))
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid carousel_id")

    carousel = db.get(Carousel, cid)
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    exp = Export(carousel_id=carousel.id, status="queued")
    db.add(exp)
    db.commit()
    db.refresh(exp)

    bg.add_task(run_export, exp.id)

    return {
        "id": str(exp.id),
        "carousel_id": str(exp.carousel_id),
        "status": exp.status,
        "error": exp.error,
    }


@router.get("/{export_id}")
def get_export(export_id: UUID, db: Session = Depends(get_db)):
    exp = db.get(Export, export_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Export not found")
    url = get_file_url(exp.zip_asset_key) if exp.zip_asset_key else None
    return {
        "id": str(exp.id),
        "carousel_id": str(exp.carousel_id),
        "status": exp.status,
        "zip_asset_key": exp.zip_asset_key,
        "download_url": url,
        "error": exp.error,
    }
