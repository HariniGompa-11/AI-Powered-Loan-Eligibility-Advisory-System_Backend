from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/users")
async def list_users():
    return {"message": "Admin users endpoint"}
