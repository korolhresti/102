
from fastapi import APIRouter
from pydantic import BaseModel
import argostranslate.package, argostranslate.translate

router = APIRouter()

class TranslationRequest(BaseModel):
    content: str
    language: str

@router.post("/translate")
async def translate(request: TranslationRequest):
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((lang for lang in installed_languages if lang.code == "en"), None)
    to_lang = next((lang for lang in installed_languages if lang.code == request.language), None)
    if from_lang and to_lang:
        translation = from_lang.get_translation(to_lang)
        return {"translated": translation.translate(request.content)}
    return {"error": "Languages not found"}
