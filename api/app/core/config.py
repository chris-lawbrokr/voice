from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "voice-api"
    DATABASE_URL: str = ""
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
