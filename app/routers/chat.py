from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.groq_service import chat_with_groq

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return chat_with_groq(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))