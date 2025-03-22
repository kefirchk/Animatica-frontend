import io

import streamlit as st
from httpx import ConnectError

from logger import logger
from utils import load_image


class App:
    def __init__(self, api_client):
        self.api_client = api_client

    async def run(self):
        st.set_page_config(page_title="Animatica")
        st.markdown("<h1 style='text-align: center;'>Animatica</h1>", unsafe_allow_html=True)
        st.write("<h3 style='text-align: center;'>Generation videos from text and images using neural networks</h3>",
                 unsafe_allow_html=True)

        name = st.text_input("Enter a text for video generation", '')
        st.write("<h4 style='text-align: center;'>or</h4>", unsafe_allow_html=True)

        img = load_image()

        _, col, _ = st.columns([1] * 2 + [0.66])
        clicked = col.button('Generate a video')

        if clicked:
            try:
                if name:
                    logger.info("Generating video from text")
                    result = await self.api_client.generate_video_from_text(name)
                    st.write("Video generated from text:", result)

                elif img:
                    logger.info("Generating video from image")
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    img_bytes.seek(0)
                    result = await self.api_client.generate_video_from_image(img_bytes)
                    st.write("Video generated from image:", result)

                else:
                    st.warning("Please provide either text or an image.")
                    logger.warning("Input data is empty")

            except ConnectError as e:
                logger.error(e)
                st.error(e)
