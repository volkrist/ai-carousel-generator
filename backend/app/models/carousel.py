from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class Carousel(Base):
    __tablename__ = "carousels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)

    source_type = Column(String)
    source_payload = Column(JSON)

    lang = Column(String)
    slides_count = Column(Integer)

    style_hint = Column(String)

    status = Column(String, default="draft")

    preview_asset_key = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
