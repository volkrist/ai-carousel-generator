from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base


class Slide(Base):
    __tablename__ = "slides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    carousel_id = Column(UUID(as_uuid=True), ForeignKey("carousels.id"))

    order = Column(Integer)

    title = Column(String)
    body = Column(String)
    footer = Column(String)
