import streamlit as st
from services.auth import AuthService
from services.resource import ResourceService

# st.set_page_config(page_title="Animatica - Auth", layout="centered")

# Load styles and templates
ResourceService.load_styles("auth.css")
main_container_template = ResourceService.load_template("auth/main_container.html")
auth_header_template = ResourceService.load_template("auth/header.html")
login_column_template = ResourceService.load_template("auth/login_column.html")
register_column_template = ResourceService.load_template("auth/register_column.html")

# Message States
if "login_error" not in st.session_state:
    st.session_state.login_error = ""
if "register_error" not in st.session_state:
    st.session_state.register_error = ""
if "register_success" not in st.session_state:
    st.session_state.register_success = ""

# Terms of Service content
TERMS_OF_SERVICE = """
**Terms of Service**

By creating an account, you agree to our Terms of Service and Privacy Policy:

1. You are responsible for maintaining the confidentiality of your account
2. You must be at least 13 years old to use this service
3. You agree not to use the service for illegal activities
4. We may terminate accounts that violate our terms
5. All content you generate must comply with our community guidelines

[View full Terms of Service](https://example.com/terms)
"""

# Main Interface
if st.session_state.get("logged_in", False):
    st.success(f"Welcome back, {st.session_state.username}!")
    st.rerun()
else:
    st.markdown(main_container_template, unsafe_allow_html=True)
    st.markdown(auth_header_template, unsafe_allow_html=True)

    # Container with Forms
    col1, col2 = st.columns(2)

    with col1:
        with st.form("login_form"):
            st.markdown(login_column_template, unsafe_allow_html=True)

            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.form_submit_button("Login", type="primary", use_container_width=True):
                if AuthService.login(st.session_state.login_username, st.session_state.login_password):
                    st.rerun()

            if st.session_state.login_error:
                st.error(st.session_state.login_error)

            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        with st.form("register_form"):
            st.markdown(register_column_template, unsafe_allow_html=True)

            new_username = st.text_input("Username", key="reg_username")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")

            # Add Terms of Service checkbox
            tos_accepted = st.checkbox(
                "I agree to the Terms of Service",
                key="tos_checkbox",
                help="You must accept the Terms of Service to register",
            )
            # Show Terms of Service expander
            with st.expander("View Terms of Service", icon=":material/description:"):
                st.markdown(TERMS_OF_SERVICE, unsafe_allow_html=True)

            if st.form_submit_button("Register", type="primary", use_container_width=True):
                if not tos_accepted:
                    st.session_state.register_error = "You must accept the Terms of Service"
                elif AuthService.register(
                    st.session_state.reg_username, st.session_state.reg_password, st.session_state.reg_confirm_password
                ):
                    st.rerun()

            if st.session_state.register_error:
                st.error(st.session_state.register_error)
            elif st.session_state.register_success:
                st.success(st.session_state.register_success)

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
