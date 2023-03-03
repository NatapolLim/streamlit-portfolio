import streamlit as st
from utils.utils import txt, txt_skills, footer, nav_page, to_bin

st.set_page_config(
    page_title="Profile Page",
    page_icon="🤩"
)

#Load CSS
with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

#Head
st.write('''
# Natapol Limpananuwat
##### Profile
''', unsafe_allow_html=True)

#Profile Image
_, c2, _ = st.columns((1,1,1))
c2.image("assets/profile/profile_img.png")


#Profile summary
c1, c2 = st.columns((3,1))
c1.write('### Summary')
with open("assets/profile/Resume_Natapol_2023-1.pdf",'rb') as pdf_file:
    PDFbyte = pdf_file.read()
c2.download_button(label='Download Resume',
    data=PDFbyte,
    file_name="Resume_Natapol.pdf",
    mime='application/octet-stream')

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
txt_skills("Tools and Frameworks",['Streamlit','FastAPI','Pytorch','TensorFlow','Scikit-Learn','Pycaret','Airflow','Tableau'])
txt_skills("Infrastructure & Cloud Services", ["Docker", "AWS (S3, Glue, Athena, EC2)"])

st.markdown("""<hr class="style1">""", unsafe_allow_html=True)

# Projects preview
st.markdown('''### Projects''')


# Project
txt("""<p id="head_project">Video Content Analytics app</p>""", "Mar 2023")
_, c1, c2 = st.columns((0.1,1,2))

# c1.image("assets/face_blur/test_gif.GIF")
c2.markdown("""
- Extract features from YouTube videos using Multi-Objects Tracking and predict type of contents
- Collected Data and Fine-tuned Facenet model for main moderator detection of particular chanel
- Display metrics which analyzed from video and analyze features in order to get insights
""", unsafe_allow_html=True)
# c1.button("Try App", on_click=nav_page, args=('Face_Blur',))
st.markdown("""<hr class="style2">""", unsafe_allow_html=True)


#Project1
txt("""<p id="head_project">Face Recognition app</p>""", "Feb 2023")
_, c1, c2 = st.columns((0.1,1,2))

c1.image("assets/profile/face_rec_example.GIF")
c2.markdown("""
- Build a Face Recognition system web app using <kbd>Streamlit</kbd> framework with
- Implemented MTCNN algorithm for Face Detection and encode face image by InceptionResNet model which pre-trained on VGGFace2 dataset
- Compare face similarity through euclidean distance
""", unsafe_allow_html=True)
c1.button("Try App", on_click=nav_page, args=('Face_Recognition',), key='face_rec_page')
st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

#Project2
txt("""<p id="head_project">Face Blur app</p>""", "Feb 2023")
_, c1, c2 = st.columns((0.1,1,2))

c1.image("assets/profile/demo_face_blur.GIF")
c2.markdown("""
- Build a Face Blur web app using <kbd>Streamlit</kbd> framework
- Implemented MTCNN for Face Deteciton and designed flow of using application
""", unsafe_allow_html=True)
c1.button("Try App", on_click=nav_page, args=('Face_Blur',), key='face_blur_page')
st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

#Project3
txt("""<p id="head_project">Real-time sales analytics and implemented ETL pipeline for retail store </p>""", "Dec 2022")
_, c1 = st.columns((0.1,3))
c1.markdown("""
- Generate mock transactions to the <kbd>Kafka</kbd> topic and store the data in <kbd>S3 Bucket</kbd>
- Extracts metadata which in <kbd>S3</kbd> and stores it in Data Catalog using <kbd>Glue crawler</kbd>
- Designed real-time sales dashboard using <kbd>Tableau</kbd> from the query result of <kbd>Athena</kbd>
- Performed end-to-end <kbd>ETL pipeline</kbd> to extract data from landing zone <kbd>S3 Bucket</kbd>, transform date with features engineering using <kbd>PySpark</kbd> and load the data into processed folder with parquet format using <kbd>Airflow</kbd> to orchestrate the pipeline 
""", unsafe_allow_html=True)

st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

#Project4
txt("""<p id="head_project">Customer Segmentation of cosmetic transaction</p>""", "Apr 2022")
_, c1, c2 = st.columns((0.1,1,2))

c2.markdown("""
- Implement data cleaning and data preprocessing to raw data
- Apply <kbd>Cohort Analysis</kbd> to analyze customer behavior and <kbd>RFM Analysis</kbd> to identify the customer segment
- Visualize the top 3 category products in each segment and the correlation between category products for cross selling strategy
""", unsafe_allow_html=True)

st.markdown("""<hr class="style2">""", unsafe_allow_html=True)

#Project5
txt("""<p id="head_project">Structure designed and built a mobile base robot</p>""", "Feb 2022")
_, c1, c2 = st.columns((0.1,1,2))
c1.image("assets/profile/senior_project.jpg")
c2.markdown("""
- Determine fabrication process of components and choose standardized parts for cost reduction 
- Designed parts using <kbd>Fusion 360</kbd> and applied with <kbd>Finite Element Analysis</kbd> for validation designing
- Built <kbd>3D Printing</kbd> rapid prototypes for proofs-of-concept before CNC
- Redesigned parts to minimize size as possible for the CNC and improved <kbd>Design For Assemble</kbd>
""", unsafe_allow_html=True)

c1.button("Read More", on_click=nav_page, args=('Mechanical_Design',))
c1.caption('About Mechanical Projects')

with st.sidebar:
    footer()
footer()




