from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ai_base_url: str
    ai_model: str
    ai_api_key: str
    ai_system_prompt: str
    ai_timeout: float

    model_config = SettingsConfigDict(env_file=".env")