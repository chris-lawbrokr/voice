from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rails_base_url: str
    rails_internal_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
