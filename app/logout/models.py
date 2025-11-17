from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class LogoutSession(Base):
    __tablename__ = "logout_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    email = Column(String, index=True)
    logout_time = Column(DateTime, default=datetime.utcnow)
    session_duration = Column(Integer)  # in minutes