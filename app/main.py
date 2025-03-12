import io
import streamlit as st
from PIL import Image

def load_image():
    uploaded_file = st.file_uploader(label="Choose an image for video generation")
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None

st.set_page_config(page_title="Animatica")
st.markdown(
    "<h1 style='text-align: center;'>Animatica</h1>",
    unsafe_allow_html=True
)
st.write(
    "<h3 style='text-align: center;'>Generation videos from text and images using neural networks</h3>",
    unsafe_allow_html=True
)
name = st.text_input("Enter a text for video generation", '')
st.write(
    "<h4 style='text-align: center;'>or</h4>",
    unsafe_allow_html=True
)

img = load_image()

_, col, _ = st.columns([1]*2+[0.66])
clicked = col.button('Generate a video')
