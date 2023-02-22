import os
import shutil
import torch
import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

from utils.utils import change_state_bool, change_state_text, footer
from utils.utils_face_recognition import PreProcesssPipeline, CompareFacesPipeline

st.set_page_config(
    page_title="Face Recognition Project",
    page_icon="🤩"
)

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

DATA_MAP_PATH = "assets/face_recognition/data_store/data_map/data_map.csv"
DATA_STORE_DIR = "assets/face_recognition/data_store"

def add_face_to_database(name_: str, face_features_: torch.Tensor, face_img_: Image) -> None:
    '''Add face features to database and mapping with name.'''
    # Load data
    map_df_ = pd.read_csv(DATA_MAP_PATH)
    index = map_df_.shape[0]
    filename = os.path.join(DATA_STORE_DIR, "tensors", f'{index}_{name_}.pt')
    # Add row and save
    torch.save(face_features_, filename)
    row = pd.DataFrame({'name':[name_],'filename':[filename]})
    map_df_ = pd.concat([map_df_, row], axis=0, ignore_index=True)
    map_df_.to_csv(DATA_MAP_PATH, index=0)
    face_img_.save(os.path.join(DATA_STORE_DIR, "pictures", f'{index}_{name_}.jpg'))
    # Change state
    change_state_text(state_key='FR_state', state='add_success')

def reset_face_on_database() -> None:
    '''Reset data in data_map.csv file.'''
    ls_dir = ['pictures', 'tensors', 'data_map']
    for dir_ in ls_dir:
        dir_name = os.path.join(DATA_STORE_DIR, dir_)
        shutil.rmtree(dir_name)
        shutil.copytree(os.path.join(DATA_STORE_DIR, 'back_up',dir_), dir_name)
    # Notice that Success
    st.success("Reset Success")

# Initiate variables
if 'FR_state' not in st.session_state:
    st.session_state.camera_status = True
    st.session_state.FR_state = 'example'

# with st.sidebar:
#     choose = option_menu(
#         "Content",
#         ['App','Info'],
#         icons=['image', 'camera-video'],
#         menu_icon=None, default_index=0,
#         styles={
#             "container": {"padding": "5!important", "background-color": "#ffffff00"},
#             "icon": {"color": "white", "font-size": "14px"},
#             "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#dddddd30"},
#             "nav-link-selected": {"background-color": "#dddddd60"},
#         },
#         orientation='horizontal',
#         key='input_option',
#         )

choose = option_menu("Dev Face Recognition", ['Check-In','Faces in Database','Add Face'],
                        icons=['check-square', 'box-arrow-down','image'],
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

WEBCAM = 'Off' if st.session_state.camera_status else "On"

if choose=='Check-In':
    with st.expander(label='Image Input', expanded=True):
        st.caption('Select input source Example Image, Webcam or Upload Image')

        example_imgs = {'Elon':'assets/face_recognition/example_faces/elon_musk/3.jpg',
                'Code':'assets/face_recognition/example_faces/codedy/4.jpg',
                }
        example_name = st.selectbox(label='Example images',
            options=example_imgs,
            index=0,
            on_change=change_state_text,
            args=('FR_state','example'))

        c1, c2 = st.columns(2)
        img = c1.camera_input("Webcam Status : "+WEBCAM,
                key='webcam',
                on_change=change_state_text,
                args=('FR_state','webcam'),
                disabled=st.session_state.camera_status,
                )
        file = c2.file_uploader(
            "Upload File Here",
            type=['jpg','png'],
            on_change=change_state_text,
            args=('FR_state','upload',),
            key='upload_img'
            )
        c1, c2 = c1.columns(2)
        c1.button("Open Camera", on_click=change_state_bool, args=('camera_status',False,))
        c2.button("Stop Camera", on_click=change_state_bool, args=('camera_status',True,))

    #select final img
    if st.session_state.FR_state=='example':
        img = Image.open(example_imgs[example_name])
    elif st.session_state.FR_state=='webcam':
        img = st.session_state.backup_img
    elif st.session_state.FR_state=='upload':
        if isinstance(file, type(None)):
            st.error('Please upload face or use webcam camera.')
            st.stop()
        else:
            img = Image.open(file)

    pre_process = PreProcesssPipeline()

    if st.session_state.FR_state in ['example', 'webcam', 'upload']:
        st.session_state.FR_main_img = img
        with st.expander(label="Image input : "+st.session_state.FR_state, expanded=True):
            c1, c2 = st.columns(2)
            face_img, label_img = pre_process.extract_face_img(img)
            if face_img is not None:
                c1.write('Label Face')
                c1.image(label_img)
                c2.write('Cropped Face')
                c2.image(face_img)
                st.button(
                    "Process",
                    key='process_dist_btn',
                    on_click=change_state_text,
                    args=('FR_state', 'process'),
                    use_container_width=True
                    )
            else:
                st.error('Image has no face, please try another image.')
                st.stop()

    if st.session_state.FR_state=='process':
        img = st.session_state.FR_main_img
        face, label_img = pre_process.extract_face_img(img)
        face_features = pre_process.encode_face(img)

        process_dist = CompareFacesPipeline(face_features)
        idx, dist = process_dist.compare_faces(face_features, return_dist=True)
        status, name, face_img = process_dist.get_info(process_dist.all_faces, idx)

        with st.expander(label='Result', expanded=True):
            if status == 1:
                c1, c2, c3 = st.columns((1,1,1))
                c1.write('Input Image')
                c1.image(face)
                c2.write('Data Image')
                c2.image(face_img)
                c3.write('Name')
                c3.subheader(name)
                st.success('Face match!')
            else:
                c1, c2 = st.columns(2)
                c1.subheader('Label Face')
                c1.image(label_img, width=300)
                c2.subheader('Cropped Face')
                c2.image(face)
                st.error("Face didn't match")
            # st.write(dist)

elif choose=='Faces in Database':
    map_df = pd.read_csv(DATA_MAP_PATH)
    c1, c2 = st.columns((3,1))
    c1.metric(label='Number Faces', value=map_df.shape[0])
    if c2.button('Reset All Faces', key='clear_btn'):
        c2.button('Summit', on_click=reset_face_on_database, key='make_sure_btn')
    st.write(map_df)

elif choose=='Add Face':
    with st.expander(label="Image Input", expanded=True):
        st.caption('Select input source Webcam or Upload Image')
        c1, c2 = st.columns(2)
        img = c1.camera_input(
            "Please take a picture | Webcam Status : "+WEBCAM,
            key='webcam_add_face',
            on_change=change_state_text,
            args=('FR_state', 'webcam_add_face',),
            disabled=st.session_state.camera_status)
        c1.caption('Please select Open/Stop camera manually')
        file = c2.file_uploader(
            "Upload File Here",
            type=['jpg','png'],
            on_change=change_state_text,
            args=('FR_state','upload',),
            key='upload_img')
        c1, c2 = c1.columns(2)
        c1.button("Open Camera", on_click=change_state_bool, args=('camera_status',False,))
        c2.button("Stop Camera", on_click=change_state_bool, args=('camera_status',True,))

    #select final img
    if st.session_state.FR_state=='webcam_add_face':
        img = st.session_state.backup_img
    elif st.session_state.FR_state=='upload':
        img = Image.open(file)

    if st.session_state.FR_state in ['webcam_add_face', 'upload']:
        with st.expander(label='Register', expanded=True):
            process = PreProcesssPipeline()
            c1, c2 = st.columns(2)
            face, label_img = process.extract_face_img(img)
            if face is not None:
                c1.subheader('Label Face')
                c1.image(label_img)
                c2.subheader('Cropped Face')
                c2.image(face)
                face_features = process.encode_face(img)
                name = st.text_input(label='Name', key='name')
                if name:
                    st.button(
                        "Add Face",
                        on_click=add_face_to_database,
                        args=(name, face_features, face[0]),
                        use_container_width=True
                        )
                else:
                    st.caption('Please fill "Name"')
            else:
                st.error('Image has no face, please try again.')
                st.stop()
    if st.session_state.FR_state=='add_success':
        st.success("Add Face Success!")
footer()
