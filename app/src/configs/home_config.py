from pydantic import Field
from pydantic_settings import BaseSettings


class HomeConfig(BaseSettings):
    PLACEHOLDER_TEXT: str = Field("Describe what you want to generate...")
    ALLOWED_IMAGE_TYPES: list = ["jpg", "jpeg", "png"]
