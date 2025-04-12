from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIConfig(BaseSettings):
    BASE_URL: str = Field(..., alias="API_URL")
    TERMS_OF_SERVICE_URL: str = Field(..., alias="TERMS_OF_SERVICE_URL")

    model_config = SettingsConfigDict(env_file="../env/api.env")
