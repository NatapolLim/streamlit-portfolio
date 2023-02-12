from apps import face_blur, profile
from multiapp import MultiApp
import streamlit as st

st.set_page_config(
    page_title="Yoyo-Profile",
    layout='centered',
    page_icon= "🤩",
)
app = MultiApp()

app.add_app("Profile Page", profile.app)
app.add_app("Face Blur Project", face_blur.app)

app.run()