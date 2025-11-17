# # app/contact/models.py
# from sqlalchemy import Column, Integer, String, Date, Text
# from sqlalchemy.types import JSON
# from app.database import Base  # shared Base

# class Contact(Base):
#     __tablename__ = "contacts"
#     id = Column(Integer, primary_key=True, index=True)   # contact primary id
#     first_name = Column(String(100), nullable=False)
#     last_name = Column(String(100), nullable=True)
#     address = Column(Text, nullable=True)
#     designation = Column(String(100), nullable=True)
#     phone_number = Column(String(50), nullable=True)
#     dob = Column(Date, nullable=True)
#     email = Column(String(256), nullable=True)

#     image_path = Column(String(512), nullable=True)
#     center_photos = Column(JSON, nullable=True)
#     logo_path = Column(String(512), nullable=True)
#     other_activities_path = Column(String(512), nullable=True)


# class InaiCredential(Base):
#     __tablename__ = "inai_credentials"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, index=True)                 # keep user_id for INAI
#     username = Column(String(256), nullable=False)
#     password_encrypted = Column(String(1024), nullable=False)









# app/contact/models.py
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.types import JSON
from app.database import Base  # shared Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)   # contact primary id (auto-generated)
    # aid removed
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    designation = Column(String(100), nullable=True)
    phone_number = Column(String(50), nullable=True)
    dob = Column(Date, nullable=True)

    # uploads
    image_path = Column(String(512), nullable=True)
    center_photos = Column(JSON, nullable=True)
    logo_path = Column(String(512), nullable=True)
    other_activities_path = Column(String(512), nullable=True)

    # INAI fields (stored with encrypted password)
    inai_email = Column(String(256), nullable=True)
    inai_password_encrypted = Column(String(1024), nullable=True)
