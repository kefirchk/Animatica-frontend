import time

import streamlit as st
from configs import APIConfig
from services.auth import AuthService
from services.cookie import CookieService


class PricingRender:
    def __init__(self, templates: dict):
        self.templates = templates
        self.auth_service = AuthService()
        self.cookie = CookieService.controller
        self.api_config = APIConfig()
        self._init_session_state()
        self._handle_payment_callback()
        self.stripe_public_key, self.products = self._load_products()

    @staticmethod
    def _init_session_state():
        if "selected_product_id" not in st.session_state:
            st.session_state.selected_product_id = None
        if "selected_price_id" not in st.session_state:
            st.session_state.selected_price_id = None

    def _handle_payment_callback(self):
        def reload():
            st.query_params.clear()
            time.sleep(3)
            st.rerun()

        if st.query_params.get("success") == "true":
            st.success("✅ Payment was successful! Thank you for your purchase!")
            if self.cookie.get("session_id") and self.cookie.get("product_id"):
                self._handle_successful_payment()
                reload()

        elif st.query_params.get("canceled") == "true":
            st.warning("❌ Payment canceled")
            reload()

    def _handle_successful_payment(self):
        response = self.auth_service.make_authenticated_request(
            "POST",
            f"{self.api_config.BASE_URL}/api/v0/payments",
            json={
                "session_id": self.cookie.get("session_id"),
                "product_id": self.cookie.get("product_id"),
            },
        )
        if response.status_code == 200:
            data = response.json()
            self.cookie.set("query_balance", data["remaining_queries"], max_age=31556925)
        else:
            st.error(f"Payment failed: {response.json()}")
            time.sleep(3)

    def _load_products(self):
        response = self.auth_service.make_authenticated_request(
            "GET", f"{self.api_config.BASE_URL}/api/v0/subscriptions/limited"
        )
        data = response.json()
        return data.get("public_key"), data.get("data", [])

    def _select_product(self, product_id: str, price_id: str):
        st.session_state.selected_product_id = product_id
        st.session_state.selected_price_id = price_id
        self.cookie.set("price_id", price_id, max_age=31556925)

    def render_plan_card(self, product, col):
        with col:
            product_id = product["id"]
            price_id = product["default_price"]["id"]
            is_selected = st.session_state.selected_product_id == product_id

            st.button(
                product["name"].removeprefix("Animatica "),
                key=f"plan_btn_{product_id}",
                type="primary" if is_selected else "secondary",
                use_container_width=True,
                on_click=self._select_product,
                args=(product_id, price_id),
            )

            features_html = "".join(
                f'<li class="plan-feature">{feature["name"]}</li>' for feature in product["marketing_features"]
            )

            st.markdown(
                self.templates["plan_card"].format(
                    card_class="plan-card selected" if is_selected else "plan-card",
                    plan_name=product["name"].removeprefix("Animatica "),
                    price=f"${product['default_price']['unit_amount'] / 100}",
                    discount=(
                        f"Discount {product['default_price']['metadata'].get('discount', '')}%"
                        if product["default_price"]["metadata"].get("discount")
                        else ""
                    ),
                    features=features_html,
                ),
                unsafe_allow_html=True,
            )

    def render_subscribe_button(self, selected_product):
        st.markdown(
            self.templates["selection"].format(selected_plan=selected_product["name"]),
            unsafe_allow_html=True,
        )

        response = self.auth_service.make_authenticated_request(
            "POST",
            f"{self.api_config.BASE_URL}/api/v0/payments/checkout-session",
            params={"price_id": st.session_state.selected_price_id},
        )
        self.cookie.set("product_id", st.session_state.selected_product_id, max_age=31556925)

        if response.status_code == 200:
            checkout_session = response.json()["checkout_session"]
            template = self.templates["checkout_button"].format(url=checkout_session["url"])
            st.markdown(template, unsafe_allow_html=True)
            self.cookie.set("session_id", checkout_session["id"], max_age=60)

        elif response.status_code == 401:
            self.auth_service.logout()
            st.switch_page("views/auth.py")

        else:
            error_msg = response.json().get("detail", "Unknown payment error")
            st.error(f"Payment error: {error_msg}")
