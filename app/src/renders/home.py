import streamlit as st
from configs import HomeConfig
from services.cookie import CookieService
from services.payment import PaymentService


class HomeRender:
    def __init__(self, templates: dict):
        self.templates = templates
        self.home_config = HomeConfig()
        query_balance = PaymentService.get_query_balance()
        CookieService.controller.set("query_balance", query_balance, max_age=31556925)
        self._init_session_state()

    @staticmethod
    def _init_session_state():
        if "animation_result" not in st.session_state:
            st.session_state.animation_result = None

    def render_subscription_required(self):
        st.markdown(self.templates["subscription"], unsafe_allow_html=True)
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "View Plans",
                type="primary",
                help="See subscription options",
                use_container_width=True,
            ):
                st.switch_page("views/pricing.py")

    def render_generation_form(self):
        st.markdown(self.templates["header"], unsafe_allow_html=True)
        with st.container():
            text_input = st.text_input(
                label="text_input",
                value="",
                key="text_input",
                label_visibility="collapsed",
                placeholder=self.home_config.PLACEHOLDER_TEXT,
            )

            st.markdown("""<div class="divider">or</div>""", unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                label="file_uploader",
                type=self.home_config.ALLOWED_IMAGE_TYPES,
                key="image_uploader",
                label_visibility="collapsed",
            )

            if uploaded_file:
                st.image(uploaded_file, use_column_width=True, caption="Your uploaded image")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "Generate Video",
                type="primary",
                use_container_width=True,
                help="Generate video from your text or image",
            ):
                self._process_generation_request()

    @staticmethod
    def _process_generation_request():  # TODO: change on animation
        st.session_state.animation_result = "sample_video_data"
        st.rerun()

    def render_result(self):
        if "animation_result" in st.session_state and st.session_state.animation_result:
            st.markdown(self.templates["header"], unsafe_allow_html=True)
            st.download_button(
                label="Download Video",
                data=st.session_state.animation_result,
                file_name="generated_video.mp4",
                mime="video/mp4",
            )
