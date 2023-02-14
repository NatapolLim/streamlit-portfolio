import streamlit as st
from utils import txt

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

txt("""<p id="head_project">Structure designed and built a mobile base robot</p>""", "Apr 2022")
st.image("./images/profile/senior_example.GIF")

st.markdown("""
- Determine fabrication process of components and choose standardized parts for cost reduction 
- Designed parts using <kbd>Fusion 360</kbd> and applied with <kbd>Finite Element Analysis</kbd> for validation designing
- Built <kbd>3D Printing</kbd> rapid prototypes for proofs-of-concept before CNC
- Redesigned parts to minimize size as possible for the CNC and improved <kbd>Design For Assemble</kbd>
""", unsafe_allow_html=True)

st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

st.subheader("Objective")
st.subheader("Workflow")
st.subheader("Result")