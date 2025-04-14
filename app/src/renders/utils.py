from functools import wraps

import streamlit as st
from numpy import ndarray
from PIL import Image


def centered_button(columns_config=None):
    if columns_config is None:
        columns_config = [1, 2, 1]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _, col2, _ = st.columns(columns_config)
            with col2:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def resize_and_center(image_np: ndarray, target_width: int = 320, target_height: int = 240):
    image = Image.fromarray(image_np)
    image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    new_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))
    paste_x = (target_width - image.width) // 2
    paste_y = (target_height - image.height) // 2
    new_img.paste(image, (paste_x, paste_y))
    return new_img
