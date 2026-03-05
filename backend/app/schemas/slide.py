from uuid import UUID

from pydantic import BaseModel


class SlideResponse(BaseModel):
    id: UUID
    order: int
    title: str | None
    body: str | None
    footer: str | None

    model_config = {"from_attributes": True}


class SlideUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    footer: str | None = None
