import streamlit as st
from utils.utils import nav_link

nav_link("https://natapollim-retail-analytics-and--0-customer-segmentation-e6fszl.streamlit.app")
st.write('''The customer segment page will open a new tap automatically.

    If it not work, please click button below
        ''', unsafe_allow_html=True)
st.button("Go to Customer Segment pages", on_click=nav_link, args=('https://natapollim-retail-analytics-and--0-customer-segmentation-e6fszl.streamlit.app',), use_container_width=True)