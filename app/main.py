from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers import chat
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="API de assistente inteligente usando Groq + LLaMA",
    version="1.0.0"
)

app.include_router(chat.router)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "online", "app": settings.app_name}