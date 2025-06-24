
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class StartRequest(BaseModel):
    user_id: int
    language: str
    country: str
    filters: list

@router.post("/start")
async def start_user(request: StartRequest):
    return {"message": f"Користувач {request.user_id} активовано з мовою {request.language} та країною {request.country}."}
