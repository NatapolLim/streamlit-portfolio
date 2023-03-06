import streamlit as st

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

st.title('Projects Planning')


st.subheader('Customer Segmentation')
st.write('''
- Migrating from notebook
- General Questions EDA
- Features: Cohort Analysis, RFM, Segmentation
- Plotly Vistualization
- Churn Prediction: modeling, tuning
''')
st.caption('Implementing...')

st.subheader('Video Content Analytics')
st.write('''
- Design main algorithm
- Preform Shot boundary detection in order to divide video into sub-videos base on cut scene
- Test and see the result preformance of object tracking to sub-videos
- Attemp to research scene recognition
- Form data input for classification model to classify type of content
- Research Multimodal: Audio and Text
''')
st.caption('Implementing...')
st.markdown('---') 

st.subheader('Wating lists')
st.write('''
- Preform A/B testing
- Aspect-base sentiment analysis
- E-commerce Chatbot
- Recommendation System
- OCR Lisense plate or Docs
- Summarize news
- Dashboard StockPrice
- Speech Recognition
- Reinforcement Learning
''', unsafe_allow_html=True)

