import streamlit as st
from services.auth import AuthService
from services.payment import PaymentService
from services.resource import ResourceService
from views import about_page, auth_page, home_page, pricing_page

ResourceService.load_styles("sidebar.css")
credit_card_template = ResourceService.load_template("sidebar/credit_card.html")


def render_sidebar():
    with st.sidebar:
        st.logo("src/assets/images/animatica_logo.png", size="large")

        if st.session_state.logged_in:
            remaining_queries = PaymentService.get_query_balance()
            st.markdown(credit_card_template.format(credits=remaining_queries), unsafe_allow_html=True)

            if st.button(
                "Logout",
                help="Logout from your account",
                type="primary",
                use_container_width=True,
                key="sidebar_logout",
                icon=":material/logout:",
            ):
                AuthService.logout()

        st.markdown("---")
        st.caption("Made with ❤️ by [kefirchk](https://github.com/kefirchk)")


def main():
    AuthService.check_auth()

    if st.session_state.logged_in:
        pg = st.navigation(pages=[home_page, pricing_page, about_page])
        pg.run()
    else:
        st.navigation(pages=[auth_page])
        auth_page.run()

    render_sidebar()


if __name__ == "__main__":
    main()
