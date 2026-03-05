import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes import assets, carousels, design, exports, generations, slides
from app.core.database import Base, engine
from app.models import carousel, export, generation, slide  # noqa: F401 - register models
import app.models.design  # noqa: F401 - register DesignSettings


def ensure_tables():
    for attempt in range(30):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            return
        except Exception:
            time.sleep(1)
    raise RuntimeError("Could not connect to database after 30 attempts")


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_tables()
    yield


app = FastAPI(title="AI Carousel Generator", lifespan=lifespan)
app.include_router(carousels.router)
app.include_router(slides.router)
app.include_router(generations.router)
app.include_router(design.router)
app.include_router(assets.router)
app.include_router(exports.router)


@app.get("/")
def root():
    return {"status": "ok"}
