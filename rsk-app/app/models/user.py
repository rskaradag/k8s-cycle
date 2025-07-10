from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import db

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    full_name = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)

    resource_requests = relationship("ResourceRequest", back_populates="user", cascade="all, delete-orphan")