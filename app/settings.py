from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rails_base_url: str
    rails_internal_api_key: str

    twilio_account_sid: str
    twilio_api_key_sid: str
    twilio_api_key_secret: str
    twilio_phone_number: str

    openai_api_key: str

    # Public URL for Twilio webhooks (e.g. ngrok URL)
    public_base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()
