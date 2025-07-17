import base64
import streamlit as st
import os

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_file):
    if not os.path.exists(image_file):
        st.warning(f"Background image '{image_file}' not found.")
        return

    # Infer MIME type
    ext = os.path.splitext(image_file)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    bin_str = get_base64(image_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:{mime};base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
