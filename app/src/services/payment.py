import time

import streamlit as st
from configs.api import APIConfig
from configs.pricing import PricingConfig
from services.auth import AuthService
from services.cookie import CookieService


class PaymentService:
    api_config = APIConfig()
    pricing_config = PricingConfig()

    @classmethod
    def get_query_balance(cls):
        current_subscription_response = AuthService.make_authenticated_request(
            "GET",
            f"{cls.api_config.BASE_URL}/api/v0/subscriptions/current",
        )
        if current_subscription_response.status_code == 200:
            subscription = current_subscription_response.json()["subscription"]
            remaining_queries = subscription.get("remaining_queries", 0) if subscription else 0
            return remaining_queries
        else:
            st.error("Can't get remaining queries!")
            AuthService.logout()

    @classmethod
    def make_payment(cls):
        response = AuthService.make_authenticated_request(
            "POST",
            f"{cls.api_config.BASE_URL}/api/v0/payments",
            json={
                "session_id": CookieService.controller.get("session_id"),
                "product_id": CookieService.controller.get("product_id"),
            },
        )
        if response.status_code == 200:
            data = response.json()
            CookieService.controller.set("query_balance", data["remaining_queries"], max_age=31556925)
        else:
            st.error(f"Payment failed: {response.json()}")
            time.sleep(cls.pricing_config.MESSAGE_DELAY)
