
from apps import face_blur
import streamlit as st
from PIL import Image
import numpy as np
import base64
import os


#Thank for GokulNC
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url, size=30, circle=False):
    img_cls= ''
    if circle:
        img_cls = "rounded-circle"
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img class="{img_cls}" src="data:image/{img_format};base64,{bin_str}" width="{size}" height="{size}"/>
        </a>'''
    return html_code

def txt(a, b):
    col1, col2 = st.columns([4,1])
    with col1:
        st.markdown(a, unsafe_allow_html=True)
    with col2:
        st.markdown(b)

def txt_skills(topic, skills):
    col1, col2 = st.columns([1,3])
    with col1:
        st.markdown(topic)
    with col2:
        text=""""""
        for skill in skills:
            text+=f"<kbd>{skill}</kbd>"
            text+=', '
        
        st.markdown(text[:-2], unsafe_allow_html=True)

def to_page_(page):
    st.session_state.page = page

def app():

    with open("src/profile/style.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
    st.markdown("""
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #787878;">
    <a class="navbar-brand" href="https://www.linkedin.com/in/natapol-limpananuwat-686595202" target="_blank">Natapol Limpananuwat</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
        <li class="nav-item active">
            <a class="nav-link disabled" href="/">Home <span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#education">Education</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#skills">Skills</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#projects">Projects</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#contact">Contact</a>
        </li>
        </ul>
    </div>
    </nav>
    """, unsafe_allow_html=True)

    st.write('''
    # Natapol Limpananuwat
    ##### Profile
    ''')


    #Profile Image
    c1, c2, c3 = st.columns((1,1,1))
    c1.write("  ")
    c2.image("src/profile/profile_img_2.png")
    c3.write("  ")

    #Profile summary
    st.markdown('''### Summary''')
    st.markdown("""
    Hello, my name is Natapol Limpananuwat. I graduated from mechanical engineering major at Chulalongkorn University. Although I am still in the early stages of my career, I am passionate about machine learning and have been actively learning and exploring the field. I have taken courses on DataCamp, and I have also completed several data science projects using various tools and techniques to gain a deeper understanding of the concepts and best practices in data science. Through my projects, I have gained knowledge in fundamental of end-to-end Machine Learning  project such as Data manipulation and cleaning, Machine learning algorithms, Deep learning frameworks, Cloud Technologies and so on.""",
    unsafe_allow_html=True)

    
    #Education
    st.markdown('''### Education''')
    txt("""
    Chulalongkorn University | Bachelor’s Degree<br>
    Mechanical Engineering | GPA = 2.89""",
    "2018-2022"
    )
    st.markdown("", unsafe_allow_html=True)

    #Skills
    st.markdown('''### Skills''')
    txt_skills("Programming",['Python', 'SQL', 'Linux'])
    txt_skills("DeepLearning", ["Framework","TensorFlow", "Pytorch"])
    txt_skills("API Framework",['FastAPI'])
    txt_skills("App Framework",['Stramlit'])

    st.markdown("""<hr class="style1">""", unsafe_allow_html=True)
    #projects preview
    st.markdown('''### Projects''')

    with st.container():
        
        st.markdown("""<p id="head_project">Face Blur app</p>""", unsafe_allow_html=True)
        _, c1, c2 = st.columns((0.1,1,2))
        c1.image("src/profile/face_blur_img.png")
        c2.markdown("""
        - asdf
        - asdf
        - asdf
        """)
    with st.container():
        st.markdown("""<p id="head_project">Real-time sales analytics and implement ETL pipeline for retail store </p>""", unsafe_allow_html=True)
        _, c1, c2 = st.columns((0.1,1,2))
        c2.markdown("""
        - Generate mock transactions to the <kbd>Kafka</kbd> topic and store the data in <kbd>S3 Bucket</kbd>
        - Extracts metadata which in S3 and stores it in Data Catalog using <kbd>Glue crawler</kbd>
        - Designed real-time sales dashboard using <kbd>Tableau</kbd> from the query result of <kbd>Athena</kbd>
        - Performed end-to-end <kbd>ETL pipeline</kbd> to extract data from landing zone <kbd>S3 Bucket</kbd>, transform date with features engineering using <kbd>PySpark</kbd> and load the data into processed folder with parquet format using <kbd>Airflow</kbd> to orchestrate the pipeline 
        """, unsafe_allow_html=True)
        # st.markdown("""<kbd>Use</kbd>, <kbd>Use</kbd>""", unsafe_allow_html=True)
    








    #contact
    st.markdown('''#### Contact''')
    c1, c2 ,c3, c4 = st.columns((3,1,1,3))

    linkedin_img_html = get_img_with_href(
        'src/profile/640px-LinkedIn_logo_initials.png',
        'https://www.linkedin.com/in/natapol-limpananuwat-686595202'
        )
    c2.markdown(linkedin_img_html, unsafe_allow_html=True)

    github_img_html = get_img_with_href(
        'src/profile/1164606_telegram-icon-github-icon-png-white-png-download.png-removebg-preview.png',
        'https://github.com/NatapolLim'
        )
    c3.markdown(github_img_html, unsafe_allow_html=True)

    c1, c2 ,c3 = st.columns((1,3,1))

    c2.markdown("""<p id='footer'>
    Address: Bangkoknoi Bangkok 10700</br>
    Email: Natapolllim@gmail.com</br>
    Tel: 084-926-7299
    </p>
    """, unsafe_allow_html=True)

    
    


