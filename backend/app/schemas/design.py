from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

Template = Literal["classic", "bold", "minimal"]
BgType = Literal["color", "image"]
AlignH = Literal["left", "center", "right"]
AlignV = Literal["top", "center", "bottom"]


class DesignUpdate(BaseModel):
    template: Template | None = None

    bg_type: BgType | None = None
    bg_color: str | None = None
    bg_image_key: str | None = None
    bg_dim: float | None = Field(default=None, ge=0.0, le=1.0)

    layout_padding: int | None = Field(default=None, ge=0, le=200)
    align_h: AlignH | None = None
    align_v: AlignV | None = None

    show_header: bool | None = None
    header_text: str | None = None

    show_footer: bool | None = None
    footer_text: str | None = None


class DesignResponse(BaseModel):
    carousel_id: UUID
    template: str
    bg_type: str
    bg_color: str
    bg_image_key: str | None
    bg_dim: float
    layout_padding: int
    align_h: str
    align_v: str
    show_header: bool
    header_text: str | None
    show_footer: bool
    footer_text: str | None

    model_config = {"from_attributes": True}
