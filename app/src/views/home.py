import io
import logging

import streamlit as st
from httpx import ConnectError
from services.resource import ResourceService

logger = logging.getLogger(__name__)

# st.set_page_config(page_title="Home - Animatica", layout="centered")

# Load styles and templates
ResourceService.load_styles("home.css")
subscription_template = ResourceService.load_template("home/subscription_required.html")
header_template = ResourceService.load_template("home/generation_header.html")
result_template = ResourceService.load_template("home/result_container.html")

# Check subscription
if "trial" not in st.session_state and "subscribe" not in st.session_state:
    st.markdown(subscription_template, unsafe_allow_html=True)

    # Buttons in columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        cols = st.columns(2)
        with cols[0]:
            if st.button(
                "Try Free", type="primary", help="Start with free trial", key="trial_btn", use_container_width=True
            ):
                st.session_state.trial = True
                st.rerun()

        with cols[1]:
            if st.button(
                "View Plans",
                type="secondary",
                help="See subscription options",
                key="plans_btn",
                use_container_width=True,
            ):
                st.switch_page("views/pricing.py")
else:
    st.markdown(header_template, unsafe_allow_html=True)

    # Main Content
    with st.container():
        # Text Input Section
        text_input = st.text_input(
            "Describe what you want to generate...",
            "",
            key="text_input",
            label_visibility="collapsed",
            placeholder="Describe what you want to generate...",
        )

        st.markdown("""<div class="divider">or</div>""", unsafe_allow_html=True)

        # Load Image Section
        uploaded_file = st.file_uploader(
            "Upload an image", type=["jpg", "jpeg", "png"], key="image_uploader", label_visibility="collapsed"
        )

        if uploaded_file is not None:
            st.image(uploaded_file, use_column_width=True, caption="Your uploaded image", output_format="PNG")

    # Generate Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_clicked = st.button(
            "Generate Video",
            key="generate_btn",
            type="primary",
            use_container_width=True,
            help="Generate video from your text or image",
        )

    # Processing of generating
    if generate_clicked:
        text_input = st.session_state.get("text_input", "")
        uploaded_file = st.session_state.get("image_uploader", None)

        try:
            if text_input:
                logger.info("Generating video from text")
                with st.spinner("Creating your video..."):
                    st.success("Video generated successfully from text!")

            elif uploaded_file is not None:
                logger.info("Generating video from image")
                with st.spinner("Animating your image..."):
                    img_bytes = io.BytesIO(uploaded_file.getvalue())
                    st.success("Video generated successfully from image!")

            else:
                st.warning("Please provide either text or an image.")
                logger.warning("Input data is empty")

        except ConnectError as e:
            logger.error(e)
            st.error("Connection error. Please try again later.")

    # If there's a result of generating
    if "generation_result" in st.session_state:
        st.markdown(result_template, unsafe_allow_html=True)
        st.download_button(
            label="Download Video",
            data=st.session_state.generation_result,
            file_name="generated_video.mp4",
            mime="video/mp4",
        )
