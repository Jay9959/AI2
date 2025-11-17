# from pydantic import BaseModel, EmailStr, constr, validator

# class ForgotPasswordRequest(BaseModel):
#     email: EmailStr

# class ResetPasswordRequest(BaseModel):
#     new_password: constr(min_length=6, max_length=72)
#     confirm_password: constr(min_length=6, max_length=72)

#     @validator("confirm_password")
#     def passwords_match(cls, v, values):
#         if "new_password" in values and v != values["new_password"]:
#             raise ValueError("Passwords do not match")
#         return v


from pydantic import BaseModel, EmailStr, constr, validator

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    new_password: constr(min_length=6, max_length=72)
    confirm_password: constr(min_length=6, max_length=72)

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v

