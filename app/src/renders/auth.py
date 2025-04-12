import streamlit as st
from configs import AuthConfig
from services.auth import AuthService


class AuthRender:
    def __init__(self, templates: dict):
        self.templates = templates
        self.auth_service = AuthService()
        self.auth_config = AuthConfig()
        self._init_session_state()

    @staticmethod
    def _init_session_state():
        if "login_error" not in st.session_state:
            st.session_state.login_error = ""
        if "register_error" not in st.session_state:
            st.session_state.register_error = ""
        if "register_success" not in st.session_state:
            st.session_state.register_success = ""

    def render_login_form(self):
        with st.form("login_form"):
            st.markdown(self.templates["login_column"], unsafe_allow_html=True)

            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.form_submit_button("Login", type="primary", use_container_width=True):
                if self.auth_service.login(username, password):
                    st.rerun()

            if st.session_state.login_error:
                st.error(st.session_state.login_error)

            st.markdown("</div>", unsafe_allow_html=True)

    def render_register_form(self):
        with st.form("register_form"):
            st.markdown(self.templates["register_column"], unsafe_allow_html=True)

            new_username = st.text_input("Username", key="reg_username")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")

            tos_accepted = st.checkbox(
                "I agree to the Terms of Service",
                key="tos_checkbox",
                help="You must accept the Terms of Service to register",
            )

            with st.expander("View Terms of Service", icon=":material/description:"):
                st.markdown(self.auth_config.TERMS_OF_SERVICE, unsafe_allow_html=True)

            if st.form_submit_button("Register", type="primary", use_container_width=True):
                if not tos_accepted:
                    st.session_state.register_error = "You must accept the Terms of Service"
                elif self.auth_service.register(new_username, new_password, confirm_password):
                    st.rerun()

            if st.session_state.register_error:
                st.error(st.session_state.register_error)
            elif st.session_state.register_success:
                st.success(st.session_state.register_success)

            st.markdown("</div>", unsafe_allow_html=True)
