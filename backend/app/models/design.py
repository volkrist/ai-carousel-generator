from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class DesignSettings(Base):
    __tablename__ = "design_settings"

    carousel_id = Column(
        UUID(as_uuid=True), ForeignKey("carousels.id"), primary_key=True
    )

    template = Column(String, default="classic")  # classic/bold/minimal

    bg_type = Column(String, default="color")  # color/image
    bg_color = Column(String, default="#ffffff")
    bg_image_key = Column(String, nullable=True)
    bg_dim = Column(Float, default=0.0)  # 0..1

    layout_padding = Column(Integer, default=24)  # px-like
    align_h = Column(String, default="center")  # left/center/right
    align_v = Column(String, default="center")  # top/center/bottom

    show_header = Column(Boolean, default=False)
    header_text = Column(String, nullable=True)

    show_footer = Column(Boolean, default=True)
    footer_text = Column(String, nullable=True)
