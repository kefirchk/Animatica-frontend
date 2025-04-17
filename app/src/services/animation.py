from configs import APIConfig
from services.auth import AuthService


class AnimationService:
    def __init__(self):
        self.api_url = APIConfig().BASE_URL
        self.auth_service = AuthService()

    def generate_animation(self, files: dict):
        try:
            response = self.auth_service.make_authenticated_request(
                "POST",
                f"{self.api_url}/api/v0/animation/video",
                files=files,
                timeout=300,
            )
            response.raise_for_status()
            return {"success": True, "animation_data": response.content, "message": "OK"}
        except Exception as e:
            return {"success": False, "animation_data": None, "message": str(e)}
