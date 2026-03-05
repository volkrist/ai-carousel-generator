from uuid import UUID

from pydantic import BaseModel, Field


class SlideLLM(BaseModel):
    order: int = Field(..., ge=1)
    title: str = Field(..., max_length=80)
    body: str = Field(..., max_length=420)
    footer: str | None = Field(default=None, max_length=120)


class GenerationResult(BaseModel):
    slides: list[SlideLLM]


class GenerationCreate(BaseModel):
    carousel_id: UUID
    model: str = "gpt-4o-mini"


class GenerationResponse(BaseModel):
    id: UUID
    carousel_id: UUID
    status: str
    error: str | None = None

    model_config = {"from_attributes": True}
