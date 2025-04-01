import streamlit as st
from services.auth import AuthService
from views import about_page, auth_page, home_page, pricing_page

# st.set_page_config(page_title="Animatica - Auth", layout="centered")

AuthService.check_auth()

# Navigation menu
if st.session_state.logged_in:
    pg = st.navigation(pages=[home_page, pricing_page, about_page])
    pg.run()
    if st.sidebar.button("Logout", help="Logout from your account", type="primary", use_container_width=True):
        AuthService.logout()
else:
    pg = st.navigation(pages=[auth_page])
    auth_page.run()


# Setting up Sidebar
st.logo("app/src/assets/images/animatica_logo.png", size="large")
st.sidebar.markdown("Made with ❤️ by [kefirchk](https://github.com/kefirchk)")
