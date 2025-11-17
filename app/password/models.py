from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class PasswordChangeLog(Base):
    __tablename__ = "change_password"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    email = Column(String, index=True)
    change_time = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    success = Column(String, default="true")  # "true" or "false"