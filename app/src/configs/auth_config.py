from configs.api_config import APIConfig
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    TERMS_OF_SERVICE: str = f"""
    **Terms of Service**
    
    By creating an account, you agree to our Terms of Service and Privacy Policy:
    
    1. You are responsible for maintaining the confidentiality of your account
    2. You must be at least 13 years old to use this service
    3. You agree not to use the service for illegal activities
    4. We may terminate accounts that violate our terms
    5. All content you generate must comply with our community guidelines
    
    [View full Terms of Service]({APIConfig().TERMS_OF_SERVICE_URL})
    """
