import streamlit as st

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

st.markdown("### coming soon", unsafe_allow_html=True)