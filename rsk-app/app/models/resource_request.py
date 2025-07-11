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
    resource_request_id = Column(String(10), unique=True, nullable=False)
    request_name = Column(Text)
    resource_url = Column(Text, nullable=False)
    status = Column(String(32), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resource_requests")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "resource_request_id": self.resource_request_id,
            "request_name": self.request_name,
            "resource_url": self.resource_url,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }