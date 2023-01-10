import streamlit as st
import pandas as pd
import os
from pycaret.regression import setup, compare_models, pull, save_model
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from PIL import Image
import numpy as np
# from pycaret.classification import setup, compare_models, pull, save_model, load_model


if os.path.exists("sourcedata.csv"):
    df = pd.read_csv("sourcedata.csv",index_col=None)

with st.sidebar:
    
    st.title("AutoML")
    choice = st.selectbox(
        'Navigation',
            ["Profile",
            "ETL-project",
            "Customer-Segmentation-and-Churn-Prediction",
            'Upload',
            'Profiling',
            'ML',
            'Download']
        )
    st.info("This is application allows you to build an AutoML")
if choice == "Profile":
    st.title("Natapol Limapanuwat")
    c1,c2 = st.columns((1,1))
    with c1:
        st.image("/Users/natapollimpananuwat/Downloads/IMG_8551_1.jpg",width=300)
    with c2:
        st.text("This is my profile")
        img_file_buffer = st.camera_input("Take a picture")
        if img_file_buffer is not None:
            img = Image.open(img_file_buffer)
            img_array = np.array(img)
            st.write(type(img_array))
            st.write(img_array.shape)
        st.video("/Users/natapollimpananuwat/Desktop/3.mp4")
        st.success('This is a success message!', icon="✅")
elif choice == "ETL-project":
    pass
elif choice == "Customer-Segmentation-and-Churn-Prediction":
    pass


elif choice == "Upload":
    st.title("Upload Youre Data for Modelling")
    file = st.file_uploader("Upload Your Dataset Here!!")
    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv("sourcedata.csv", index=None)
        st.dataframe(df)

elif choice =="Profiling":
    st.title("Automate Exploratory Data Analysis")
    profile_report = df.profile_report()
    st_profile_report(profile_report)


elif choice=="ML":
    st.title("Machine Learning")
    target = st.selectbox("Select Your Target", df.columns)
    if st.button("Run Modelling"):
        
        setup(df,target=target)
        set_up = pull()
        best_model = compare_models()
        compare_df = pull()
        st.dataframe(compare_df)
        save_model(best_model,"best_model")

elif choice=="Download":
    with open("best_model.pkl",'rb') as f:
        st.download_button("Download Model", f, file_name= "best_model.pkl")