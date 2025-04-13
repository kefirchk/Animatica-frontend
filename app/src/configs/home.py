from pydantic import Field
from pydantic_settings import BaseSettings


class HomeConfig(BaseSettings):
    ALLOWED_IMAGE_TYPES: list = ["jpg", "jpeg", "png"]
    ALLOWED_VIDEO_TYPES: list = ["mp4", "mov", "avi"]
    MESSAGE_DELAY: int = Field(3)
