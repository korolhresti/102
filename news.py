
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.utils.db import get_db

router = APIRouter()

class NewsItem(BaseModel):
    id: int
    title: str
    content: str
    created_at: str

@router.get("/news", response_model=List[NewsItem])
async def get_news():
    conn = await get_db()
    rows = await conn.fetch("SELECT id, title, content, created_at FROM news ORDER BY created_at DESC LIMIT 20")
    return [dict(row) for row in rows]
