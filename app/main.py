from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.signup import models as signup_models
from app.password import models as password_models
from app.database import engine

from app.signup.auth_routes import router as signup_router
from app.login.routes import router as login_router
from app.logout.routes import router as logout_router
from app.password.change_password_routes import router as password_router
from app.forgot_password import routes as forgot_password

app = FastAPI(
    title="INAI Authentication API",
    description="Signup, Login, Logout, and Password Change System",
    version="1.0.1"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(signup_router)
app.include_router(login_router)
app.include_router(logout_router)
app.include_router(password_router)
app.include_router(forgot_password.router)

# Database Tables
signup_models.Base.metadata.create_all(bind=engine)
password_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "🚀 INAI Authentication API Running Successfully!"}
