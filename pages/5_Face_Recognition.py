from streamlit_option_menu import option_menu
from facenet_pytorch import MTCNN, InceptionResnetV1
import streamlit as st
from PIL import Image
import cv2
import torch
import numpy as np
from utils.utils import get_faces_img, draw
from utils.utils_face_recognition import PreProcesssPipeline
import pandas as pd
import os
import shutil

DATA_MAP_PATH = "images/face_recognition/data_store/data_map.csv"
DATA_STORE_DIR = "images/face_recognition/data_store"

def add_face_to_database(name_: str, face_features_: torch.Tensor, face_img: Image) -> None:
    '''Add face features to database and mapping with name'''
    #Load data
    map_df_ = pd.read_csv(DATA_MAP_PATH)
    index = map_df_.shape[0]
    filename = os.path.join(DATA_STORE_DIR, "tensors", f'{index}_{name_}.pt')
    #Add row and save
    torch.save(face_features_, filename)
    row = pd.DataFrame({'name':[name_],'filename':[filename]})
    map_df_ = pd.concat([map_df_, row], axis=0, ignore_index=True)
    map_df_.to_csv(DATA_MAP_PATH, index=0)
    face_img.save(os.path.join(DATA_STORE_DIR, "pictures", f'{index}_{name_}.jpg'))
    #Notice that Success
    change_state_text(state_key='state', state='add_success')
    st.success("Add Face Success!")

def clear_face_on_database() -> None:
    '''Clear data in data_map.csv file'''
    map_df_ = pd.DataFrame(columns=['name','filename'])
    map_df_.to_csv(DATA_MAP_PATH, index=0)
    ls_dir = ['pictures', 'tensors']
    for dir_ in ls_dir:
        dir_name = os.path.join(DATA_STORE_DIR, dir_)
        shutil.rmtree(dir_name)
        os.mkdir(dir_name)
    st.info("Delete Success")

def match_face(face_features: torch.Tensor):
    #load data from txt -> mapping, feature store
    
    pass

def backup_img(key: str) -> None:
    '''Backup image from webcam and Check in case webcam is closed, then do not backup again'''
    if st.session_state[key] is not None:
        _img = st.session_state[key]
        st.session_state.webcam_img = Image.open(_img).copy()
        st.session_state.camera_status = True

def call_back_tasks(order: list) -> None:
    pass
    
def change_state_text(state_key: str, state: str) -> None:
    '''Change State from callback fucntion follow the state input.'''
    st.session_state[state_key] = state

    if state in ['webcam','webcam_add_face']:
        backup_img(state)
        st.session_state.expand_webcam = False

        

def change_state_bool(state_key: str,state: bool) -> None:
    '''Change State from callback fucntion follow the state input.'''
    st.session_state[state_key] = state

    if state_key == 'camera_status' and state==False:
        st.session_state.expand_webcam = True


if 'state' not in st.session_state:
    st.session_state.camera_status = True
    st.session_state.expand_webcam = False  
    st.session_state.state = 'example'

with st.sidebar:
    choose = option_menu(
        "Content",
        ['App','Info'],
        icons=['image', 'camera-video'],
        menu_icon=None, default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#ffffff00"},
            "icon": {"color": "white", "font-size": "14px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#dddddd30"},
            "nav-link-selected": {"background-color": "#dddddd60"},
        },
        orientation='horizontal',
        key='input_option',
        )

choose = option_menu("Dev Face Recognition", ['Check-In','Faces in Database','Add Face'],
                        icons=['image', 'camera-video','youtube'],
                        menu_icon=None, default_index=0,
                        styles={
        "container": {"padding": "5!important", "background-color": "#ffffff00"},
        "icon": {"color": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#dddddd30"},
        "nav-link-selected": {"background-color": "#dddddd60"},
        },
        orientation='horizontal',
        key='features'
        )

webcam_status = 'Off' if st.session_state.camera_status else "On"

if choose=='Check-In':
    # with st.expander(label="Camera Input"):
    with st.sidebar:
        file = st.file_uploader("Upload File Here", type=['jpg'], on_change=change_state_text, args=('state','upload',), key='upload_img')
        st.markdown(st.session_state.state)
    
    with st.expander(label="Webcam Status : "+webcam_status, expanded=st.session_state.expand_webcam):
        img = st.camera_input("",
                key='webcam',
                on_change=change_state_text,
                args=('state','webcam'),
                disabled=st.session_state.camera_status,
                )
        c1, c2, _ = st.columns((1,1,3))
        c1.button("Open Camera", on_click=change_state_bool, args=('camera_status',False,))
        c2.button("Stop Camera", on_click=change_state_bool, args=('camera_status',True,))
    
    
    #select final img
    if st.session_state.state=='example':
        img = Image.open("images/face_recognition/yo.jpg")
    elif st.session_state.state=='webcam':
        img = st.session_state.webcam_img
    elif st.session_state.state=='upload':
        img = Image.open(file)

    process = PreProcesssPipeline()

    if img is not None:
        with st.expander(label=f"Output of {st.session_state.state} image",expanded=True):
            c1, c2 = st.columns(2)
            main_img = c1.empty()
            main_img.image(img)
            face, label_img = process.extract_face_img(img)
            main_img.image(label_img)
            c2.subheader('Face')
            c2.image(face)
            face_features = process.encode_face(img)
            
            # st.session_state.state = 'processed'

    #Process find distance
    if True:
        name = 'test1'
        st.success(f"Welcom {name}!!!")
    else:
        st.error("Sorry, please try again.")
        # c2.write(st.session_state.embedding_value)

elif choose=='Faces in Database':
    map_df = pd.read_csv(DATA_MAP_PATH)
    c1, c2 = st.columns((3,1))
    c1.metric(label='Number Faces', value=map_df.shape[0])
    if c2.button('Clear All Faces', key='clear_btn'):
        c2.button('Summit', on_click=clear_face_on_database, key='make_sure_btn')
    
    st.write(map_df)

elif choose=='Add Face':
    with st.sidebar:
        file = st.file_uploader("Upload File Here", type=['jpg'], on_change=change_state_text, args=('state','upload',), key='upload_img')
        st.markdown(st.session_state.state)

    with st.expander(label="Webcam Status : "+webcam_status, expanded=True):
        img = st.camera_input(
            "Please take a picture",
            key='webcam_add_face',
            on_change=change_state_text,
            args=('state', 'webcam_add_face',),
            disabled=st.session_state.camera_status)
        st.caption('Please select Open/Stop camera manually')
        c1, c2, _ = st.columns((1,1,3))
        c1.button("Open Camera", on_click=change_state_bool, args=('camera_status',False,))
        c2.button("Stop Camera", on_click=change_state_bool, args=('camera_status',True,))

    #select final img

    if st.session_state.state=='webcam_add_face':
        img = st.session_state.webcam_img
    elif st.session_state.state=='upload':
        img = Image.open(file)


    if img is not None:
        process = PreProcesssPipeline()

        c1, c2 = st.columns(2)
        main_img = c1.empty()
        main_img.image(img)
        face, label_img = process.extract_face_img(img)
        main_img.image(label_img)
        c2.subheader('Face')
        c2.image(face)
        face_features = process.encode_face(img)

        name = st.text_input(label='Name', key='name')
        if name:
            st.button("Add Face", on_click=add_face_to_database, args=(name, face_features, face))
        else:
            st.caption('Please fill "Name"')

    # if st.session_state.state=='add_success':
    #     with st.expander(label='Result', expanded=True):
    #         img = st.session_state.webcam_img
    #         c1, c2 = st.columns((1,2))
    #         c1.image(img)
    #         c2.write(name)
        

