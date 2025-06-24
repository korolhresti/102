
from app.main import app

async def get_db():
    return await app.state.db.acquire()
