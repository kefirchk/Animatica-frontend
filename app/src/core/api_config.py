from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIConfig(BaseSettings):
    BASE_URL: str = Field("http://localhost:8080", alias="API_URL")

    model_config = SettingsConfigDict(env_file='env/api.env')

