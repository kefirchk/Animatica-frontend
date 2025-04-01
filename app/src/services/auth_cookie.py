from streamlit_cookies_controller import CookieController


class AuthCookieService:
    controller = CookieController()

    @classmethod
    def set_auth_cookies(cls, token_data: dict):
        cls.controller.set("auth_data", token_data)

    @classmethod
    def get_auth_cookies(cls) -> dict | None:
        auth_data = cls.controller.get("auth_data")
        return auth_data if auth_data else None

    @classmethod
    def clear_auth_cookies(cls):
        cls.controller.remove("auth_data")

    @classmethod
    def get_auth_headers(cls) -> dict:
        auth_data = cls.controller.get("auth_data")
        if auth_data and "access_token" in auth_data:
            return {"Authorization": f'Bearer {auth_data["access_token"]}'}
        return {}
