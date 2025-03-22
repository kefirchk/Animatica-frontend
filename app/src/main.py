import asyncio

from api_client import APIClient
from api_config import APIConfig
from app import App

if __name__ == "__main__":
    api_client = APIClient(base_url=APIConfig().BASE_URL)
    asyncio.run(App(api_client).run())
