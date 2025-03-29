import httpx


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def generate_video_from_text(self, text):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/generating/text-to-video", json={"text": text})
            return response.json()

    async def generate_video_from_image(self, image_bytes):
        async with httpx.AsyncClient() as client:
            files = {"image": ("image.png", image_bytes, "image/png")}
            response = await client.post(f"{self.base_url}/generating/image-to-video", files=files)
            return response.json()
