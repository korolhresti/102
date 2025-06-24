
from fastapi import APIRouter
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

class AnalyzeRequest(BaseModel):
    content: str

@router.post("/analyze_news")
async def analyze_news(request: AnalyzeRequest):
    messages = [
        {"role": "system", "content": "Ти аналізуєш новини: дай резюме, ключові теги й настрій."},
        {"role": "user", "content": request.content}
    ]
    response = await openai.ChatCompletion.acreate(model="gpt-4", messages=messages)
    return {"analysis": response.choices[0].message.content}
