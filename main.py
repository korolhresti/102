from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import openai
import httpx
import asyncpg
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

class NewsRequest(BaseModel):
    content: str
    language: str = "uk"

class NewsItem(BaseModel):
    id: int
    title: str
    content: str
    created_at: str

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

@app.get("/news", response_model=List[NewsItem])
async def get_news():
    async with app.state.db.acquire() as conn:
        rows = await conn.fetch("SELECT id, title, content, created_at FROM news ORDER BY created_at DESC LIMIT 20")
        return [dict(row) for row in rows]

@app.post("/analyze_news")
async def analyze_news(request: NewsRequest):
    messages = [
        {"role": "system", "content": "Ти аналізуєш новини: дай резюме, ключові теги й настрій."},
        {"role": "user", "content": request.content}
    ]
    response = await openai.ChatCompletion.acreate(model="gpt-4", messages=messages)
    return {"analysis": response.choices[0].message.content}

@app.post("/translate")
async def translate(request: NewsRequest):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"https://translation.googleapis.com/language/translate/v2",
            params={
                "key": GOOGLE_TRANSLATE_API_KEY,
                "q": request.content,
                "target": request.language
            }
        )
        return r.json()