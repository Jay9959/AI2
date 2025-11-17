# app/signup/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
import json

from app.database import SessionLocal
from app.signup import models
from app.signup.schemas import SignupIn, UserOut

# no prefix here; prefix added in main.py
router = APIRouter(tags=["Authentication"])


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Full package details
PACKAGE_DETAILS = {
    "p1": {
        "price": "₹20,000",
        "videos": "45 videos (1 year)",
        "max_quality": "720p",
        "max_lecture_length": "30 min",
        "ai_videos_per_lecture": 4,
        "topics_per_lecture": 2,
        "extra_credit": "₹500/lecture",
        "extra_ai_video": "₹30/video",
        "features": [
            "Basic level Q&A with AI",
            "Normal teacher visuals (inai, aira, vinai)",
            "Unlimited students browsing",
            "Every language support",
            "iOS & Android student apps",
            "0% transaction fee",
            "Global payments & taxes (included)",
            "24/7 email technical & student support",
        ],
    },
    "p2": {
        "price": "₹50,000",
        "videos": "120 videos (1 year)",
        "max_quality": "1080p",
        "max_lecture_length": "45 min",
        "ai_videos_per_lecture": 6,
        "topics_per_lecture": 5,
        "extra_credit": "₹400/lecture",
        "extra_ai_video": "₹25/video",
        "features": [
            "Logo add option",
            "AI technical lecture (basic)",
            "Free coding lectures (C, C++, React.js, HTML)",
            "200+ book suggestions",
            "20 lectures offline download",
            "Advance level Q&A with AI",
            "10% discount rate",
            "Semi realistic visuals",
            "Unlimited students browsing",
            "Every language support",
            "24/7 email & chat support",
        ],
    },
    "p3": {
        "price": "₹100,000",
        "videos": "250 videos (1 year)",
        "max_quality": "1440p",
        "max_lecture_length": "60 min",
        "ai_videos_per_lecture": 8,
        "topics_per_lecture": 10,
        "extra_credit": "₹300/lecture",
        "extra_ai_video": "₹20/video",
        "features": [
            "Deep storyline lectures",
            "Captions (English, Hindi)",
            "Logo add option",
            "AI technical lecture (researcher level)",
            "Free coding (C, C++, HTML, CSS, Java, Python, React.js)",
            "500+ books",
            "50 lectures offline download",
            "Researcher-level Q&A with AI",
            "15% student discount",
            "Hyper-realistic visuals + custom avatar",
            "Prototype updates access",
            "Unlimited students browsing",
            "24/7 email, chat & call support",
        ],
    },
}


@router.post("/signup", response_model=UserOut, status_code=201)
def signup(data: SignupIn, db: Session = Depends(get_db)):
    # Check duplicate email
    existing = db.execute(select(models.User).where(
        models.User.email == data.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check duplicate username
    existing_user = db.execute(select(models.User).where(
        models.User.username == data.username)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Validate and handle password length (bcrypt has 72-byte limit)
    password_bytes = data.password.encode('utf-8')
    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=400, detail="Password too long. Maximum 72 bytes allowed.")

    # Hash password - ensure it's within bcrypt limits
    try:
        hashed_pw = pwd_context.hash(data.password)
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            raise HTTPException(
                status_code=400, detail="Password too long. Maximum 72 bytes allowed.")
        raise HTTPException(status_code=500, detail="Password hashing failed")

    # Get package details as JSON text (optional)
    package_features = None
    if data.package:
        # data.package is a PackageEnum; use .value to get "p1"/"p2"/"p3"
        package_info = PACKAGE_DETAILS.get(data.package.value)
        if not package_info:
            raise HTTPException(status_code=400, detail="Invalid package type")
        package_features = json.dumps(package_info, ensure_ascii=False)

    # Create new user
    new_user = models.User(
        email=data.email,
        username=data.username,
        hashed_password=hashed_pw,
        role=data.role.value,
        package=data.package.value if data.package else None,
        package_features=package_features,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
