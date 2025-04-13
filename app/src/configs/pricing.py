from pydantic import Field
from pydantic_settings import BaseSettings


class PricingConfig(BaseSettings):
    MESSAGE_DELAY: int = Field(3)
