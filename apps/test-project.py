import streamlit as st

def app():
    t_choice = st.sidebar.radio("T-Test Settings",["One Sample Data","One Sample Stats","Paired Sample Data","Two Sample Data","Two Sample Stats"])
    if t_choice == "Profile":
        pass