from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import db

class ResourceRequest(db.Model):
    __tablename__ = "resource_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resource_request_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    request_name = Column(Text)
    resource_url = Column(Text, nullable=False)
    status = Column(String(32), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resource_requests")