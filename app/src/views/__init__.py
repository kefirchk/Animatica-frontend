import streamlit as st

auth_page = st.Page(
    page="views/auth.py",
    title="Authentication",
    icon=":material/login:",
)

home_page = st.Page(
    page="views/home.py",
    title="Home",
    icon=":material/home:",
)

about_page = st.Page(
    page="views/about.py",
    title="About",
    icon=":material/info:",
)

pricing_page = st.Page(
    page="views/pricing.py",
    title="Pricing",
    icon=":material/payments:",
)
