# from sqlalchemy import Column, Integer, String, DateTime
# from app.database import Base
# from datetime import datetime

# class LoginSession(Base):
#     __tablename__ = "login_sessions"
    
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, index=True)
#     email = Column(String, index=True)
#     login_time = Column(DateTime, default=datetime.utcnow)
#     ip_address = Column(String)
#     user_agent = Column(String)

from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime


class LoginSession(Base):
    __tablename__ = "login_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    email = Column(String, index=True)
    login_time = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    user_agent = Column(String)

