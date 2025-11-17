# # app/contact/schemas.py
# from pydantic import BaseModel, EmailStr, constr
# from typing import List, Optional
# from datetime import date

# # Contact: create without user_id
# class ContactCreate(BaseModel):
#     first_name: constr(min_length=1)
#     last_name: Optional[str] = None
#     address: Optional[str] = None
#     designation: Optional[str] = None
#     phone_number: Optional[str] = None
#     dob: Optional[date] = None
#     email: Optional[EmailStr] = None

# class ContactRead(BaseModel):
#     id: int
#     first_name: str
#     last_name: Optional[str]
#     address: Optional[str]
#     designation: Optional[str]
#     phone_number: Optional[str]
#     dob: Optional[date]
#     email: Optional[EmailStr]
#     image_path: Optional[str]
#     center_photos: Optional[List[str]]
#     logo_path: Optional[str]
#     other_activities_path: Optional[str]

#     class Config:
#         from_attributes = True  # pydantic v2 compatible; if using v1 use orm_mode=True

# # INAI schemas keep user_id
# class InaiCreate(BaseModel):
#     user_id: int
#     username: str
#     password: str

# class InaiRead(BaseModel):
#     user_id: int
#     username: str
#     password: Optional[str] = None

#     class Config:
#         from_attributes = True






from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional, Union
from datetime import date


# ------------------------------------------------------
# ContactCreate — for POST /contact/
# ------------------------------------------------------
class ContactCreate(BaseModel):
    first_name: constr(min_length=1)
    last_name: Optional[str] = None
    address: Optional[str] = None
    designation: Optional[str] = None
    phone_number: Optional[str] = None
    dob: Optional[date] = None
    inai_email: Optional[EmailStr] = None
    inai_password: Optional[str] = None


# ------------------------------------------------------
# ContactRead — for GET /contact/{id} or after creation
# ------------------------------------------------------
class ContactRead(BaseModel):
    aid: Optional[int] = None
    id: Optional[int] = None
    first_name: str
    last_name: Optional[str]
    address: Optional[str]
    designation: Optional[str]
    phone_number: Optional[str]
    dob: Optional[date]
    image_path: Optional[str]
    # ✅ center_photos can be a single string or a list
    center_photos: Optional[Union[str, List[str]]]
    logo_path: Optional[str]
    other_activities_path: Optional[str]
    inai_email: Optional[EmailStr]

    def model_post_init(self, __context):
        """✅ Automatically set aid = id and flatten center_photos list."""
        if not self.aid and self.id:
            self.aid = self.id

        # ✅ Convert single-item list → string
        if isinstance(self.center_photos, list):
            if len(self.center_photos) == 1:
                self.center_photos = self.center_photos[0]
            elif len(self.center_photos) == 0:
                self.center_photos = None

    class Config:
        from_attributes = True
        orm_mode = True


# ------------------------------------------------------
# InaiRead — for GET /contact/{id}/inai
# ------------------------------------------------------
class InaiRead(BaseModel):
    aid: Optional[int] = None
    id: Optional[int] = None
    inai_email: Optional[EmailStr]
    inai_password: Optional[str] = None

    def model_post_init(self, __context):
        """✅ Automatically set aid = id if not provided."""
        if not self.aid and self.id:
            self.aid = self.id

    class Config:
        from_attributes = True
        orm_mode = True
