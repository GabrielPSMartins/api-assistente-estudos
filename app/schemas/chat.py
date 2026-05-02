from pydantic import BaseModel
from typing import Literal

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    message: str
    history: list[Message] = []
    model: str | None = None

class Section(BaseModel):
    title: str
    content: str

class ResponseBody(BaseModel):
    sections: list[Section]
    summary: str

class ChatResponse(BaseModel):
    response: ResponseBody
    model: str