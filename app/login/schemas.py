# from pydantic import BaseModel, EmailStr

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

# class LoginResponse(BaseModel):
#     message: str
#     access_token: str
#     token_type: str = "bearer"

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
