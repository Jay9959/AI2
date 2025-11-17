from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.password.schemas import ChangePasswordRequest
from app.signup.models import User
from passlib.context import CryptContext
from pydantic import ValidationError
from jose import JWTError, jwt
from typing import Optional
from os import getenv

router = APIRouter(tags=["change_Password"])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

SECRET_KEY = getenv("SECRET_KEY", "supersecretinaiappkey")
ALGORITHM = "HS256"

@router.post("/change_password")
async def change_password(
    request: ChangePasswordRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

        token = authorization.split(" ", 1)[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        if request.new_password != request.confirm_password:
            raise HTTPException(status_code=422, detail="New password and confirmation do not match")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not pwd_context.verify(request.old_password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Old password is incorrect")

        if request.new_password == request.old_password:
            raise HTTPException(status_code=400, detail="New password cannot be same as old")

        if not any(c.isupper() for c in request.new_password):
            raise HTTPException(status_code=422, detail="Password must contain at least one uppercase letter")
        if not any(c.islower() for c in request.new_password):
            raise HTTPException(status_code=422, detail="Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in request.new_password):
            raise HTTPException(status_code=422, detail="Password must contain at least one number")

        password_bytes = request.new_password.encode('utf-8')
        if len(password_bytes) > 72:
            raise HTTPException(status_code=422, detail="Password too long. Maximum 72 bytes allowed.")

        hashed_new_password = pwd_context.hash(request.new_password)
        user.hashed_password = hashed_new_password

        try:
            db.commit()
            return {"message": "Password changed successfully"}
        except Exception as db_error:
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to update password in database")

    except ValidationError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")