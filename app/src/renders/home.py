import base64
import time

import numpy as np
import streamlit as st
from configs import HomeConfig
from PIL import Image
from renders.utils import centered_button, resize_and_center
from services.animation import AnimationService
from services.cookie import CookieService
from services.payment import PaymentService


class HomeRender:
    def __init__(self, templates: dict):
        self.templates = templates
        self.animation_service = AnimationService()
        self.home_config = HomeConfig()
        query_balance = PaymentService.get_query_balance()
        CookieService.controller.set("query_balance", query_balance, max_age=31556925)
        self._init_session_state()

    @staticmethod
    def _init_session_state():
        st.session_state.setdefault("animation_result", None)
        st.session_state.setdefault("source_image", None)
        st.session_state.setdefault("driving_video", None)

    @centered_button()
    def render_subscription_required(self):
        st.markdown(self.templates["subscription"], unsafe_allow_html=True)
        if st.button("View Plans", type="primary", help="See subscription options", use_container_width=True):
            st.switch_page("views/pricing.py")

    def render_image_upload(self, target_width: int = 320):
        uploaded_image = st.file_uploader(
            "Upload source image",
            type=self.home_config.ALLOWED_IMAGE_TYPES,
            key="source_uploader",
            label_visibility="collapsed",
        )
        if uploaded_image:
            st.session_state.source_image = uploaded_image.read()
            img_np = np.array(Image.open(uploaded_image).convert("RGB"))
            resized = resize_and_center(img_np)
            st.image(resized, width=target_width, caption="Source Image")

    def render_video_upload(self):
        uploaded_video = st.file_uploader(
            "Upload driving video",
            type=self.home_config.ALLOWED_VIDEO_TYPES,
            key="video_uploader",
            label_visibility="collapsed",
        )
        if uploaded_video:
            st.session_state.driving_video = uploaded_video.read()
            st.markdown(
                self.templates["driving_video"].format(
                    video_b64=base64.b64encode(st.session_state.driving_video).decode(),
                    target_width=320,
                    target_height=240,
                ),
                unsafe_allow_html=True,
            )

    @centered_button(3)
    def render_generate_button(self):
        if st.button(
            "Generate Animation",
            type="primary",
            use_container_width=True,
            disabled=not st.session_state.source_image or not st.session_state.driving_video,
            icon=":material/animated_images:",
        ):
            self._process_generation_request()

    def _process_generation_request(self):
        if not st.session_state.source_image or not st.session_state.driving_video:
            st.error("Please provide both source image and driving video")
            return

        with st.spinner("⏳ Generating animation... Please wait."):
            response = self.animation_service.generate_animation(
                {
                    "source_image": ("source.jpg", st.session_state.source_image, "image/jpeg"),
                    "driving_video": ("driving.mp4", st.session_state.driving_video, "video/mp4"),
                }
            )

        st.session_state.source_image = None
        st.session_state.driving_video = None

        if response["success"]:
            st.session_state.animation_result = response["animation_data"]
            st.success("✅ Animation generated successfully!")
            time.sleep(3)
            st.rerun()
        else:
            st.error(f"❌ Animation generation failed: {response['message']}")

    @centered_button(3)
    def render_download_button(self):
        st.download_button(
            label="Download Video",
            type="primary",
            data=st.session_state.animation_result,
            file_name="generated_animation.mp4",
            mime="video/mp4",
            use_container_width=True,
            icon=":material/download:",
        )
