import io

import streamlit as st
from PIL.Image import Image


def load_image():
    uploaded_file = st.file_uploader(label="Choose an image for video generation")
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    return None
