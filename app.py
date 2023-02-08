from apps import face_blur, profile
from multiapp import MultiApp
import streamlit as st

st.set_page_config(
    page_title="Yoyo-profile",
    layout='wide'
)
app = MultiApp()

# app.add_app("Profile Page", profile.app)
app.add_app("Face Blur", face_blur.app)

app.run()