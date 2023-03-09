import streamlit as st
from utils.utils import nav_link

nav_link("https://natapollim-video-analytics-app-5sdi7l.streamlit.app")
st.write('''The customer segment page will open a new tap automatically.

    If it not work, please click button below
        ''', unsafe_allow_html=True)
st.button("Go to Video Analytics pages", on_click=nav_link, args=('https://natapollim-video-analytics-app-5sdi7l.streamlit.app',), use_container_width=True)