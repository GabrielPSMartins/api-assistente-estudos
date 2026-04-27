from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "llama3-8b-8192"
    app_name: str = "Assistente IA"

    class Config:
        env_file = ".env"

settings = Settings()