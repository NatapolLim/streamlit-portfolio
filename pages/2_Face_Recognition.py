import os
import shutil
import torch
import pandas as pd
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils.utils import change_state_bool, change_multi_state, change_state_text, footer, load_img, load_df
from utils.utils_face_recognition import PreProcessPipeline, CompareFacesPipeline

st.set_page_config(
    page_title="Face Recognition Project",
    page_icon="🤩"
)

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

DATA_MAP_PATH = "assets/face_recognition/data_store/data_map/data_map.csv"
DATA_STORE_DIR = "assets/face_recognition/data_store"

def add_face_to_database(name_: str, face_features_: torch.Tensor, face_img_: JpegImageFile) -> None:
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
    st.session_state.FR_state = 'input'
    st.session_state.FR_img_input = 'example'

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

choose = option_menu("Face Recognition", ['Check-In','Faces in Database','Add Face'],
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
EXAMPLE_IMG = {'Elon':'assets/face_recognition/example_faces/elon_musk/3.jpg',
                'Code':'assets/face_recognition/example_faces/codedy/4.jpg',
                }
def check_in_page() -> None:
    '''Function separate pages for reducing memory'''
    with st.expander(label='Image Input', expanded=True):
        st.caption('Select input source Example Image, Webcam or Upload Image')
        tab1, tab2, tab3 = st.tabs(["Example Image", "Webcam Camera", "Upload File"])
        example_name = tab1.selectbox(label='Example images',
            options=EXAMPLE_IMG,
            index=0,
            on_change=change_multi_state,
            args=((('FR_img_input','example'),('FR_state','input')),)
            )

        img = tab2.camera_input("Webcam Status : "+WEBCAM,
                key='webcam',
                on_change=change_multi_state,
                args=((('FR_img_input','webcam'),('FR_state','input')),),
                disabled=st.session_state.camera_status,
                )
        tab2.caption('Please select Open/Stop camera manually')
        c1, c2 = tab2.columns(2)
        c1.button("Open Camera", on_click=change_state_bool, args=('camera_status',False,))
        c2.button("Stop Camera", on_click=change_state_bool, args=('camera_status',True,))

        file = tab3.file_uploader(
            "Upload File Here",
            type=['jpg','png'],
            on_change=change_multi_state,
            args=((('FR_img_input','upload'),('FR_state','input')),),
            key='upload_img'
            )
        
    #select final img
    if st.session_state.FR_img_input=='example':
        img = load_img(EXAMPLE_IMG[example_name])

    elif st.session_state.FR_img_input=='webcam':
        if isinstance(img, UploadedFile):
            img = Image.open(img)
        elif st.session_state.get('backup_img', None) is not None:
            img = st.session_state.backup_img
        else:
            st.error('Please take a picture if using webcam input.')
            st.stop()
            
    elif st.session_state.FR_img_input=='upload':
        if isinstance(file, UploadedFile):
            img = Image.open(file).convert('RGB')
        else:
            st.error('Please upload Image again.')
            st.stop()

    if st.session_state.FR_state == 'input':
        pre_process = PreProcessPipeline(img)
        with st.expander(label="Image input : "+st.session_state.FR_state, expanded=True):
            c1, c2 = st.columns(2)
            boxes = pre_process.extract_face_boxes()
            face_img, label_img = pre_process.extract_face_img(img, boxes)
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


    if st.session_state.FR_state=='process':
        pre_process = PreProcessPipeline(img)
        boxes = pre_process.extract_face_boxes()
        face, label_img = pre_process.extract_face_img(img, boxes)
        face_features = pre_process.encode_face(boxes)

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

def database_page():
    '''Function separate pages for reducing memory'''
    map_df = pd.read_csv(DATA_MAP_PATH, index_col=None)
    c1, c2 = st.columns((3,1))
    c1.metric(label='Number Faces', value=map_df.shape[0])
    if c2.button('Reset All Faces', key='clear_btn'):
        c2.button('Summit', on_click=reset_face_on_database, key='make_sure_btn')
    # st.write(map_df, unsafe_allow_html=True)
    with st.expander(label='Face images list in database', expanded=True):
        for idx in range(map_df.shape[0]):
            _, name, face_img =CompareFacesPipeline.get_info(map_df, idx)
            c1, c2 =st.columns((1,2))
            c1.image(face_img)
            c2.subheader(name)
            st.markdown('---')
    

def addface_page() -> None:
    '''Function separate pages for reducing memory'''
    with st.expander(label="Image Input", expanded=True):
        st.caption('Select input source Webcam or Upload Image')
        tab1, tab2 = st.tabs(["Webcam Camera", "Upload File"])
        img = tab1.camera_input(
            "Please take a picture | Webcam Status : "+WEBCAM,
            key='webcam_add_face',
            on_change=change_multi_state,
            args=((('FR_img_input','webcam_add_face'),('FR_state','add_face')),),
            disabled=st.session_state.camera_status)
        tab1.caption('Please select Open/Stop camera manually')
        c1, c2 = tab1.columns(2)
        c1.button("Open Camera", on_click=change_state_bool, args=('camera_status',False,))
        c2.button("Stop Camera", on_click=change_state_bool, args=('camera_status',True,))

        file = tab2.file_uploader(
            "Upload File Here",
            type=['jpg','png'],
            on_change=change_multi_state,
            args=((('FR_img_input','upload'),('FR_state','add_face')),),
            key='upload_img')

    if st.session_state.FR_img_input=='webcam_add_face':
        if isinstance(img, UploadedFile):
            img = Image.open(img)
        elif st.session_state.get('backup_img', None) is not None:
            img = st.session_state.backup_img
        else:
            st.error('Please open camera if using webcam input.')
            st.stop()
        
    elif st.session_state.FR_img_input=='upload':
        if isinstance(file, UploadedFile):
            img = Image.open(file)
        else:
            st.error('Please upload Image again.')
            st.stop()
        
    if st.session_state.FR_state=='add_face':
        with st.expander(label='Register', expanded=True):
            process_img = PreProcessPipeline(img,)
            c1, c2 = st.columns(2)
            boxes = process_img.extract_face_boxes()
            face, label_img = process_img.extract_face_img(img, boxes)
            if face is not None:
                c1.subheader('Label Face')
                c1.image(label_img)
                c2.subheader('Cropped Face')
                c2.image(face)
                face_features = process_img.encode_face(boxes)
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

if choose=='Check-In':
    check_in_page()
elif choose=='Faces in Database':
    database_page()
elif choose=='Add Face':
    addface_page()

footer()
