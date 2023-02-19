import streamlit as st
from PIL import Image
import numpy as np


st.sidebar.subheader("Customer_Segmentation")
choice = st.sidebar.selectbox(
'Details',
    ["Raw_data",
    "Customer-Segmentation-and-Churn-Prediction",]
)
if choice == "Raw_data":
    st.title("Input data")
if choice == "Customer-Segmentation-and-Churn-Prediction":
    st.title("Preprocess")

