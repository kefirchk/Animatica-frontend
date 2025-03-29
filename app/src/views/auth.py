import streamlit as st
from utils.resource_loader import ResourceLoader

st.set_page_config(page_title="Animatica - Auth", layout="centered")

# Load styles and templates
ResourceLoader.load_styles("auth.css")
main_container_template = ResourceLoader.load_template("auth/main_container.html")
auth_header_template = ResourceLoader.load_template("auth/header.html")
login_column_template = ResourceLoader.load_template("auth/login_column.html")
register_column_template = ResourceLoader.load_template("auth/register_column.html")


# TODO: Delete after adding Database
if "USER_CREDENTIALS" not in st.session_state:
    st.session_state.USER_CREDENTIALS = {"user1": "password1", "user2": "password2"}


# Message States
if "login_error" not in st.session_state:
    st.session_state.login_error = ""
if "register_error" not in st.session_state:
    st.session_state.register_error = ""
if "register_success" not in st.session_state:
    st.session_state.register_success = ""


# Login Function
def login(username: str, password: str) -> bool:
    if username in st.session_state.USER_CREDENTIALS:
        if st.session_state.USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_error = ""
            return True
    st.session_state.login_error = "Invalid username or password"
    return False


# Register Function
def register(username: str, password: str, confirm_password: str) -> bool:
    if username in st.session_state.USER_CREDENTIALS:
        st.session_state.register_error = "Username already exists"
        return False
    if password != confirm_password:
        st.session_state.register_error = "Passwords don't match"
        return False

    st.session_state.USER_CREDENTIALS[username] = password
    st.session_state.register_error = ""
    st.session_state.register_success = "Registration successful! Please login."
    return True


# Main Interface
if "logged_in" in st.session_state and st.session_state.logged_in:
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

            if st.form_submit_button("Login", type="primary"):
                if login(st.session_state.login_username, st.session_state.login_password):
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

            if st.form_submit_button("Register", type="primary"):
                if register(
                    st.session_state.reg_username, st.session_state.reg_password, st.session_state.reg_confirm_password
                ):
                    st.rerun()

            if st.session_state.register_error:
                st.error(st.session_state.register_error)
            elif st.session_state.register_success:
                st.success(st.session_state.register_success)

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
