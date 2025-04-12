import base64
from pathlib import Path

import streamlit as st


class ResourceService:
    """Loader of application resources (styles, templates, images)"""

    @staticmethod
    def load_styles(style_name: str):
        css_path = Path(__file__).parent.parent / "assets" / "styles" / style_name
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    @staticmethod
    def load_template(template_name: str):
        template_path = Path(__file__).parent.parent / "templates" / template_name
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def load_image(image_name: str):
        image_path = Path(__file__).parent.parent / "assets" / "images" / image_name
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
