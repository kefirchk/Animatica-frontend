import time

import streamlit as st
from renders.pricing import PricingRender
from services.auth import AuthService
from services.resource import ResourceService

# Load styles and templates
ResourceService.load_styles("pricing.css")
templates = {
    "header": ResourceService.load_template("pricing/header.html"),
    "plan_card": ResourceService.load_template("pricing/plan_card.html"),
    "selection": ResourceService.load_template("pricing/selection_message.html"),
    "checkout_button": ResourceService.load_template("pricing/checkout_button.html"),
}

st.markdown(templates["header"], unsafe_allow_html=True)
render = PricingRender(templates)

if not render.products:
    st.warning("No subscription plans available.")
    time.sleep(3)
    AuthService.logout()

with st.container():
    cols = st.columns(len(render.products))
    for col, product in zip(cols, render.products):
        render.render_plan_card(product, col)

if st.session_state.selected_product_id and st.session_state.selected_price_id:
    selected_product = next((p for p in render.products if p["id"] == st.session_state.selected_product_id), None)
    if selected_product:
        render.render_subscribe_button(selected_product)
