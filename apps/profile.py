import streamlit as st

def txt(a, b):
    _, col1, col2 = st.columns((0.1,4, 1))
    with col1:
        st.markdown(a, unsafe_allow_html=True)
    with col2:
        st.markdown(b, unsafe_allow_html=True)

def txt_skills(topic, skills):
    _, col1, col2 = st.columns((0.1, 1, 3))
    with col1:
        st.markdown(topic)
    with col2:
        text=""""""
        for skill in skills:
            text+=f"<kbd>{skill}</kbd>"
            text+=', '
        
        st.markdown(text[:-2], unsafe_allow_html=True)

def display_project_box():
    pass

def change_page(page):
    st.session_state.page = page
    st.session_state.btn = True

def app():

    # st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    #Head
    st.write('''
    # Natapol Limpananuwat
    ##### Profile
    ''')

    #Profile Image
    _, c2, _ = st.columns((1,1,1))
    c2.image("src/profile/profile_img.png")

    #Profile summary
    st.markdown('''### Summary''')
    c1, c2 = st.columns((0.1,4))
    c2.markdown("""
    Hello, my name is Natapol Limpananuwat. In this portfolio, you will find a showcase of my data science projects and skills I have acquired. However, I graduated from mechanical engineering at Chulalongkorn University with no experience in this particular field. Although I am still a beginner, I am eager to learn and expand my knowledge continuously through taking courses from DataCamp and implementing my personal projects. Through my projects, I have gained knowledge in fundamental of end-to-end Machine Learning  project such as Data Analysis, Machine learning algorithms, Deep learning frameworks, Cloud Technologies and so on.
    """,
    unsafe_allow_html=True)

    #Education
    st.markdown('''### Education''')
    txt("""
    Chulalongkorn University | Bachelor’s Degree<br>
    Mechanical Engineering | GPA = 2.89""",
    "2018-2022"
    )

    #Skills
    st.markdown('''### Skills''')
    txt_skills("Programming languages",['Python', 'SQL'])
    txt_skills("Technical Skills", ['Data Analysis',"Machine Learning","Deep Learning"])
    txt_skills("Tools and Frameworks",['Git','Stramlit','FastAPI','Pytorch','TensorFlow','Scikit-Learn','Pycaret','Airflow','Tableau'])
    txt_skills("Infrastructure & Cloud Services", ["Docker", "AWS (S3, Glue, Athena, EC2)"])

    st.markdown("""<hr class="style1">""", unsafe_allow_html=True)

    #Projects preview
    st.markdown('''### Projects''')

    with st.container():
        txt("""<p id="head_project">Face Blur app</p>""", "FEB 2023")
        _, c1, c2 = st.columns((0.1,1,2))

        c1.image("src/face_blur/test_gif.GIF")
        c2.markdown("""
        - Build a Face Blur web app using <kbd>Streamlit</kbd> framework
        - Implement Face Detection model from pytorch-face_recognition 
        """, unsafe_allow_html=True)
        c1.caption("Click 'Face Blur' on the left Menu Bar", unsafe_allow_html=True)
        st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

    with st.container():
        txt("""<p id="head_project">Real-time sales analytics and implement ETL pipeline for retail store </p>""", "DEC 2022")
        _, c1, c2 = st.columns((0.1,1,2))
        c2.markdown("""
        - Generate mock transactions to the <kbd>Kafka</kbd> topic and store the data in <kbd>S3 Bucket</kbd>
        - Extracts metadata which in S3 and stores it in Data Catalog using <kbd>Glue crawler</kbd>
        - Designed real-time sales dashboard using <kbd>Tableau</kbd> from the query result of <kbd>Athena</kbd>
        - Performed end-to-end <kbd>ETL pipeline</kbd> to extract data from landing zone <kbd>S3 Bucket</kbd>, transform date with features engineering using <kbd>PySpark</kbd> and load the data into processed folder with parquet format using <kbd>Airflow</kbd> to orchestrate the pipeline 
        """, unsafe_allow_html=True)

        st.markdown("""<hr class="style2">""", unsafe_allow_html=True)
    
    with st.container():
        txt("""<p id="head_project">Customer Segmentation of cosmetic transaction</p>""", "Apr 2022")
        _, c1, c2 = st.columns((0.1,1,2))

        c2.markdown("""
        - Implement data cleaning and data preprocessing to raw data
        - Apply <kbd>Cohort Analysis</kbd> to analyze customer behavior and <kbd>RFM Analysis</kbd> to identify the customer segment
        - Visualize the top 3 category products in each segment and the correlation between category products for cross selling strategy
        """, unsafe_allow_html=True)

        st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

    with st.container():
        txt("""<p id="head_project">Structure designed and built a mobile base robot</p>""", "Feb 2022")
        _, c1, c2 = st.columns((0.1,1,2))
        c1.image("src/profile/senior_project.jpg")
        c2.markdown("""
        - Determine fabrication process of components and choose standardized parts for cost reduction 
        - Designed parts using <kbd>Fusion 360</kbd> and applied with <kbd>Finite Element Analysis</kbd> for validation designing
        - Built <kbd>3D Printing</kbd> rapid prototypes for proofs-of-concept before CNC
        - Redesigned parts to minimize size as possible for the CNC and improved <kbd>Design For Assemble</kbd>
        """, unsafe_allow_html=True)

    


