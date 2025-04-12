import streamlit as st
from renders.auth import AuthRender
from services.resource import ResourceService

# Load styles and templates
ResourceService.load_styles("auth.css")
templates = {
    "main_container": ResourceService.load_template("auth/main_container.html"),
    "auth_header": ResourceService.load_template("auth/header.html"),
    "login_column": ResourceService.load_template("auth/login_column.html"),
    "register_column": ResourceService.load_template("auth/register_column.html"),
}

render = AuthRender(templates)

if st.session_state.get("logged_in", False):
    st.success(f"Welcome back, {st.session_state.username}!")
    st.rerun()

st.markdown(templates["main_container"], unsafe_allow_html=True)
st.markdown(templates["auth_header"], unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    render.render_login_form()
with col2:
    render.render_register_form()

st.markdown("</div>", unsafe_allow_html=True)
