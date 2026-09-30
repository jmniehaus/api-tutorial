from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_PATH = Path(__file__).parent / ".env"

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=ENV_PATH)

settings = Settings()
    