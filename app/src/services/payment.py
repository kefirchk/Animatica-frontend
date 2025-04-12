import streamlit as st
from configs.api_config import APIConfig
from services.auth import AuthService


class PaymentService:
    @classmethod
    def get_query_balance(cls):
        current_subscription_response = AuthService.make_authenticated_request(
            "GET",
            f"{APIConfig().BASE_URL}/api/v0/subscriptions/current",
        )
        if current_subscription_response.status_code == 200:
            subscription = current_subscription_response.json()["subscription"]
            remaining_queries = subscription.get("remaining_queries", 0) if subscription else 0
            return remaining_queries
        else:
            st.error("Can't get remaining queries!")
            AuthService.logout()
