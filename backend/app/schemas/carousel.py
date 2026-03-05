from uuid import UUID

from pydantic import BaseModel


class CarouselCreate(BaseModel):
    title: str
    source_type: str | None = None
    source_payload: dict | None = None
    lang: str | None = "ru"
    slides_count: int | None = 8
    style_hint: str | None = None


class CarouselUpdate(BaseModel):
    title: str | None = None
    lang: str | None = None
    slides_count: int | None = None
    style_hint: str | None = None
    status: str | None = None


class CarouselResponse(BaseModel):
    id: UUID
    title: str
    status: str
    lang: str | None
    slides_count: int | None

    model_config = {"from_attributes": True}
