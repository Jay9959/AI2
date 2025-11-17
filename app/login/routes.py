# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# import jwt

# from app.database import get_db
# from app.signup.models import User
# from app.login.schemas import LoginRequest, LoginResponse

# router = APIRouter( tags=["Login"])

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12, bcrypt__ident="2b")

# SECRET_KEY = "supersecretinaiappkey"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# @router.post("/", response_model=LoginResponse)
# def login(request: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == request.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="Invalid email or password")

#     if not pwd_context.verify(request.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     token_data = {"sub": user.email, "role": user.role}
#     access_token = create_access_token(token_data)

#     return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}



from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from app.database import get_db
from app.signup.models import User
from app.login.models import LoginSession
from app.login.schemas import LoginRequest, LoginResponse

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

SECRET_KEY = "supersecretinaiappkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    """Generate JWT token for login."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/", response_model=LoginResponse)
def login(request: LoginRequest, req: Request, db: Session = Depends(get_db)):
    """Login user and return JWT token."""

    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or password")

    # ✅ FIXED: Correct field name (User.hashed_password)
    if not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    token_data = {"sub": user.email, "role": user.role}
    access_token = create_access_token(token_data)

    # ✅ Optional: Save login session info
    login_session = LoginSession(
        user_id=user.id,
        email=user.email,
        ip_address=req.client.host,
        user_agent=req.headers.get("user-agent")
    )
    db.add(login_session)
    db.commit()

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }
