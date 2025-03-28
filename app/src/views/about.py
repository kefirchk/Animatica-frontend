import streamlit as st
from utils.resource_loader import ResourceLoader

st.set_page_config(page_title="About - Animatica", layout="centered")

context = {
    "image_base64": ResourceLoader.load_image("animatica_about.svg"),
    "email_link": "mailto:prostolex2004@mail.ru",
    "telegram_link": "https://t.me/keffirchk",
    "linkedin_link": "https://www.linkedin.com/in/alexey-klimovich-30744b249/",
    "developer_name": "Klimovich Alexey",
    "developer_info": "4th-year Computer Science student specializing in Computing Machines, Systems, and Networks",
}

ResourceLoader.load_styles("about.css")
template = ResourceLoader.load_template("about/about.html")
st.markdown(template.format(**context), unsafe_allow_html=True)
