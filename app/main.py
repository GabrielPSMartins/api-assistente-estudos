from fastapi import FastAPI
from app.routers import chat
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="API de assistente inteligente usando Groq + LLaMA",
    version="1.0.0"
)

app.include_router(chat.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "online", "app": settings.app_name}