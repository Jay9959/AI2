from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class ResetRequest(Base):
    __tablename__ = "reset_requests"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
