from pydantic import BaseModel, validator

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @validator("new_password")
    def validate_new_password_length(cls, v):
        if not v:
            raise ValueError("Password cannot be empty")
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError("Password too long. Maximum 72 bytes allowed.")
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if not v:
            raise ValueError("Confirm password cannot be empty")
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("New password and confirm password do not match")
        return v