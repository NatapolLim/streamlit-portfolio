import streamlit as st
from utils.utils import txt, txt_skills, footer

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

st.header('Mechanical Profile')
st.markdown('')
st.markdown('''### Domain skills''')
txt_skills("Mechanical engineering skills",['3D Printing', 'Design For Manufacture(DFM)', 'Design For Assemble(DFA)', 'Fusion 360',])

st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

st.subheader("Structure designed and built a mobile base robot")
st.image("./assets/mechanical_design/senior_example.GIF")

st.markdown("""
- Determine fabrication process of components and choose standardized parts for cost reduction 
- Designed parts using <kbd>Fusion 360</kbd> and applied with <kbd>Finite Element Analysis</kbd> for validation designing
- Built <kbd>3D Printing</kbd> rapid prototypes for proofs-of-concept before CNC
- Redesigned parts to minimize size as possible for the CNC and improved <kbd>Design For Assemble</kbd>
""", unsafe_allow_html=True)

st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

st.subheader("Built robotic arm and implemented object detection on Raspberry Pi")
_, c1, c2 = st.columns((0.1,1,2))
c1.image("assets/mechanical_design/IOT_project.png")
c2.markdown('''
- Implemented camera calibration code for precision of object position
- Built open-source robot arm using <kbd>3D Printing</kbd> and assemble in order to grab objects for enhancement performance between robot arm and deep learning
- Deploy <kbd>Object detection</kbd> model(.TFlite) on<kbd> Raspberry Pi</kbd>
''', unsafe_allow_html=True)

st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

st.subheader("Automatic faucet Wash+Soap+Hand Dryer")
_, c1, c2 = st.columns((0.1,1,2))
c1.image("assets/mechanical_design/Mecha_project.JPG")
c2.markdown('''
- Designed the faucet based on <kbd>DFA</kbd> which fabricated by <kbd>3D Printing</kbd> and pneumatic flow system to control the operation
- Implemented circuit design and selected proper equipment
- Built <kbd>Mediapipe</kbd> (Python library) for hand detection app to control all function of the faucet by using hand gesture and deploy on <kbd>Raspberry Pi</kbd>
''', unsafe_allow_html=True)

st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

footer()