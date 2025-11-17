from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class PackageEnum(str, Enum):
    p1 = "p1"
    p2 = "p2"
    p3 = "p3"

class SignupIn(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=128)
    role: RoleEnum
    package: Optional[PackageEnum] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: RoleEnum
    package: Optional[str] = None

    class Config:
        from_attributes = True
