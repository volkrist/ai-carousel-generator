from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class Export(Base):
    __tablename__ = "exports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    carousel_id = Column(UUID(as_uuid=True), ForeignKey("carousels.id"))

    status = Column(String, default="queued")

    zip_asset_key = Column(String)

    error = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True))
