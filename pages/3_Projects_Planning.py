import streamlit as st

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

st.title('Projects Planning')

st.subheader('Face Blur Video')
st.write('''
- **Key Blur another people without main characters**
- perform face recognition model for embedding face
- vistualize encoding in 2dim-space
- Clustering main character by number of point
- or save/train face recogniton before inference, log with MLflow?
- video to see an outcome
''')

st.subheader('Customer Segmentation')
st.write('''
- using stepper bar?
- pandas profiling?
- migrate from notebook
- General Questions EDA
- Features: Cohort Analysis, RFM, Segmentation
- Plotly Vistualization
- Churn Prediction: modeling, tuning
''')

st.subheader('OCR Lisense plate or Docs')
st.write('''
- Find Best Practice and fine-tuning
''')

st.subheader('Recommendation System')
st.subheader('Aspect-base sentiment analysis')
st.subheader('Preform A/B testing from ? datasource')
st.subheader('E-commerce Chatbot')
st.subheader('Summarize news')
st.subheader('Text to Image')
st.subheader('Dashboard show StockPrice? update everyday using airflow control task and perform some time-series model')
st.write('''
- Component: Airflow, Streamlit, Time-series model
''')

st.subheader('Analysis news classify type compare engagement (Social Listening)')
st.subheader("Speech Recognition")
st.subheader('Reinforcement Learning')

