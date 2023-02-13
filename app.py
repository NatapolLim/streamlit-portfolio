from apps import face_blur, profile, project_planning
from multiapp import MultiApp, footer
import streamlit as st

st.set_page_config(
    page_title="Yoyo-Profile",
    layout='centered',
    page_icon= ":grinning_face_with_star_eyes:",
)
app = MultiApp()

app.add_app("Profile", profile.app)
app.add_app("Face Blur", face_blur.app)
app.add_app("Project Planning", project_planning.app)

app.run()
footer()