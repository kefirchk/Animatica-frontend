import streamlit as st
from views import about_page, auth_page, home_page, pricing_page


# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.success("Successfully logged out!")
    st.rerun()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Navigation menu
if st.session_state.logged_in:
    pg = st.navigation(pages=[home_page, pricing_page, about_page])
    pg.run()
    if st.sidebar.button("Logout", help="Logout from your account", type="primary", use_container_width=True):
        logout()
else:
    pg = st.navigation(pages=[auth_page])
    auth_page.run()


# Setting up Sidebar
st.logo("app/src/assets/images/animatica_logo.png", size="large")
st.sidebar.markdown("Made with ❤️ by [kefirchk](https://github.com/kefirchk)")
