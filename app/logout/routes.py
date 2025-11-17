from fastapi import APIRouter

router = APIRouter(tags=["Logout"])

@router.post("/")
def logout():
    return {"message": "User logged out successfully (token invalidation not implemented in demo)"}
