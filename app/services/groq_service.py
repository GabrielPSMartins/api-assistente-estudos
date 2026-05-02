from groq import Groq
from app.config import settings
from app.schemas.chat import Message, ChatRequest, ChatResponse

client = Groq(api_key=settings.groq_api_key)

def chat_with_groq(request: ChatRequest) -> ChatResponse:

    model = request.model or settings.groq_model

    messages = [
        {"role": "system", "content": settings.default_system_prompt}
    ]

    for msg in request.history:
        messages.append({"role": msg.role, "content": msg.content})

    messages.append({"role": "user", "content": request.message})

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )

    ai_response = completion.choices[0].message.content

    updated_history = list(request.history)
    updated_history.append(Message(role="user", content=request.message))
    updated_history.append(Message(role="assistant", content=ai_response))

    return ChatResponse(response=ai_response, history=updated_history)