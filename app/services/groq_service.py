import re
from groq import Groq
from app.config import settings
from app.schemas.chat import Message, ChatRequest, ChatResponse, ResponseBody, Section

client = Groq(api_key=settings.groq_api_key)

def parse_markdown_to_sections(text: str) -> tuple[list[Section], str]:
    sections = []
    parts = re.split(r'###\s+', text.strip())

    for part in parts:
        if not part.strip():
            continue
        lines = part.strip().split('\n', 1)
        title = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        sections.append(Section(title=title, content=content))

    summary = sections[-1].content[:100] + "..." if sections else "Sem resumo disponível."

    return sections, summary


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

    raw_response = completion.choices[0].message.content

    sections, summary = parse_markdown_to_sections(raw_response)
    response_body = ResponseBody(sections=sections, summary=summary)

    return ChatResponse(response=response_body, model=model)