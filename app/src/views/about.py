import streamlit as st
from services.resource import ResourceService

context = {
    "image_base64": ResourceService.load_image("animatica_about.svg"),
    "email_link": "mailto:prostolex2004@mail.ru",
    "telegram_link": "https://t.me/keffirchk",
    "linkedin_link": "https://www.linkedin.com/in/alexey-klimovich-30744b249/",
    "developer_name": "Klimovich Alexey",
    "developer_info": "4th-year Computer Science student specializing in Computing Machines, Systems, and Networks",
}

ResourceService.load_styles("about.css")
template = ResourceService.load_template("about/about.html")
st.markdown(template.format(**context), unsafe_allow_html=True)
