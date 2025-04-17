import streamlit as st
from renders.home import HomeRender
from services.cookie import CookieService
from services.resource import ResourceService

# Load styles and templates
ResourceService.load_styles("home.css")
templates = {
    "subscription": ResourceService.load_template("home/subscription_required.html"),
    "driving_video": ResourceService.load_template("home/driving_video.html"),
    "header": ResourceService.load_template("home/generation_header.html"),
}

render = HomeRender(templates)
query_balance = CookieService.controller.get("query_balance")

# Check subscription
if (query_balance is None or query_balance == 0) and not st.session_state.animation_result:
    render.render_subscription_required()
else:
    st.markdown(templates["header"], unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        render.render_image_upload()
    with col2:
        render.render_video_upload()

    st.markdown("---")
    render.render_generate_button()

    if st.session_state.animation_result:
        st.markdown(templates["header"], unsafe_allow_html=True)
        st.video(st.session_state.animation_result)
        render.render_download_button()
