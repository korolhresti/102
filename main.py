
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import news, translate, analyze, users
import asyncpg
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

# Підключення роутів
app.include_router(news.router, prefix="/api")
app.include_router(translate.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(users.router, prefix="/api")
