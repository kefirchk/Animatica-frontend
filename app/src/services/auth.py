import requests
import streamlit as st
from configs.api_config import APIConfig
from services.cookie import CookieService


class AuthService:
    @staticmethod
    def check_auth():
        if "logged_in" not in st.session_state:
            auth_data = CookieService.get_auth_cookies()
            if auth_data:
                try:
                    st.session_state.update(
                        {
                            "logged_in": True,
                            "username": auth_data.get("username", ""),
                            "access_token": auth_data["access_token"],
                            "refresh_token": auth_data["refresh_token"],
                        }
                    )
                except:
                    CookieService.clear_auth_cookies()
                    st.session_state.logged_in = False
            else:
                st.session_state.logged_in = False

    @staticmethod
    def login(username: str, password: str) -> bool:
        try:
            response = requests.post(
                f"{APIConfig().BASE_URL}/api/v0/auth/login", json={"username": username, "password": password}
            )

            if response.status_code == 200:
                token_data = response.json()
                token_data["username"] = username
                st.session_state.logged_in = True
                st.session_state.username = username
                CookieService.set_auth_cookies(token_data)
                st.session_state.login_error = ""
                return True
            else:
                error_msg = (
                    response.json()["detail"][0]["msg"] if isinstance(response.json(), dict) else response.json()
                )
                st.session_state.login_error = error_msg
                return False
        except requests.exceptions.RequestException as e:
            st.session_state.login_error = f"Connection error: {str(e)}"
            return False

    @staticmethod
    def register(username: str, password: str, confirm_password: str) -> bool:
        if password != confirm_password:
            st.session_state.register_error = "Passwords don't match"
            return False

        try:
            response = requests.post(
                f"{APIConfig().BASE_URL}/api/v0/auth/signup", json={"username": username, "password": password}
            )

            if response.status_code == 201:
                st.session_state.register_error = ""
                st.session_state.register_success = "Registration successful! Please login."
                return True
            else:
                error_msg = (
                    response.json()["detail"][0]["msg"] if isinstance(response.json(), dict) else response.json()
                )
                st.session_state.register_error = error_msg
                return False
        except requests.exceptions.RequestException as e:
            st.session_state.register_error = f"Connection error: {str(e)}"
            return False

    @staticmethod
    def logout():
        st.session_state.logged_in = False
        CookieService.clear_auth_cookies()
        st.rerun()

    @staticmethod
    def make_authenticated_request(method: str, url: str, **kwargs):
        headers = CookieService.get_auth_headers()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers

        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code == 401:
                CookieService.clear_auth_cookies()
                st.session_state.logged_in = False
            return response
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
            return None
