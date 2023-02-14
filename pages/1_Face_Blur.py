from facenet_pytorch import MTCNN
from utils import resize_box, gauss_blur_face, footer
from PIL import Image, ImageDraw
import streamlit as st
import pandas as pd
import numpy as np
import torch
import time
import cv2

st.set_page_config(
    page_title="Face Blur Project",
    page_icon="🤩"
)

EXAMPLE_IMG_PATH = "images/face_blur/example1.jpg"
BLUR_IMG_PATH = "images/face_blur/Blur_img.jpg"

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

@st.cache(suppress_st_warning=True)
def processing_img(img, threshold=0.8, min_face_size=50):
    
    mtcnn = MTCNN(
            image_size=160,
            margin=20,
            min_face_size=min_face_size,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=True,
            keep_all=True,
            device=torch.device('cpu')
        )

    batch_boxes, batch_probs, _ = mtcnn.detect(img, landmarks=True)
    if batch_boxes is not None:
        boxes = []
        for box, prob in zip(batch_boxes, batch_probs):
            if prob<threshold:
                continue
            else:
                boxes.append(box)
    return boxes

@st.cache(suppress_st_warning=True)
def get_label_img(img, boxes):
    label_img = img.copy()
    draw = ImageDraw.Draw(label_img)
    for box in boxes:
        draw.rectangle(box.tolist(), outline=(255, 0, 0), width = 6)
    return label_img

@st.cache(suppress_st_warning=True)
def get_faces_img(img, boxes, img_size = 160):
    faces_img = []
    img = np.array(img)
    boxes = resize_box(img.shape, boxes, margin =10)

    for box in boxes:
        x1, y1, x2, y2 = box
        face = img[y1:y2 ,x1:x2]
        face = cv2.resize(
            face,
            (img_size, img_size),
            interpolation=cv2.INTER_AREA
            ).copy()
        faces_img.append(Image.fromarray(face))
    return faces_img

def get_blur_img(img, boxes, select_lis, ksize):
    img = np.array(img)
    boxes = resize_box(img.shape, boxes, margin =20)
    for (selected, _), box in zip(select_lis, boxes):
        if not selected:
                continue
        else:
            img = gauss_blur_face(box, img, ksize)
    return Image.fromarray(img)
    
def to_state(state):
    st.session_state.state = state


st.markdown("## Face Blur", unsafe_allow_html=True)

if 'state' not in st.session_state:
    img = Image.open(EXAMPLE_IMG_PATH)
    st.session_state.state = 'upload'
    st.session_state.img = img
    st.session_state.label_img = img
    st.session_state.boxes = None
    st.session_state.faces_img = None
    st.session_state.n_faces = 0
    st.session_state.blur_img = img
    st.session_state.caption = 'Example Image'

#layout  
step_1 = st.expander("Upload Your Image", expanded = False)
step_2 = st.expander("Detected Face Output", expanded = True)
step_3 = st.expander("Select Faces to Blur", expanded = True)
step_4 = st.expander("Blured Image", expanded = True)

col1, col2 = step_2.columns((3,1))
display_main_img = col1.empty()
display_n_faces = col2.empty()

file = step_1.file_uploader("", type=['jpg'], on_change=to_state, args=('upload',))
if file:
    img = Image.open(file)
    if st.session_state.state=='upload':
        st.session_state.caption='Uploaded Image'
        st.session_state.img = img
        st.session_state.blur_img = img
        st.session_state.n_faces = 0

img = st.session_state.img
n_faces = st.session_state.n_faces

display_main_img.image(img, caption=st.session_state.caption)
display_n_faces.metric("Detected Faces", value = n_faces)


with st.sidebar:
    st.subheader("Face Detect Config")
    threshold = st.slider(
        "Confidence",
        min_value=50,
        max_value= 99,
        value=80,
        step=1)
    min_face_size = st.slider(
        'Minimum Face Size in the Image',
        min_value=10,
        max_value=100,
        value=50,
        step=1
    )
    st.caption('Click "Process" button for apply config values')
    
if step_2.button('Process', on_click=to_state, args=('select',)):
    boxes= processing_img(img, threshold=threshold/100, min_face_size=min_face_size)
    if boxes is None:
        st.error('Image have no face!, please upload new Image')
        st.session_state.state = 'error'
    else:
        label_img = get_label_img(img, boxes)
        faces_img = get_faces_img(img, boxes)
        n_faces = len(boxes)

        st.session_state.boxes = boxes
        st.session_state.faces_img = faces_img
        st.session_state.label_img = label_img
        st.session_state.n_faces = n_faces
        st.session_state.caption = 'Labeled Image'


if st.session_state.state!='upload' and st.session_state.state!='error':
    img = st.session_state.img
    boxes = st.session_state.boxes
    faces_img = st.session_state.faces_img
    label_img = st.session_state.label_img
    n_faces = st.session_state.n_faces
    blur_img = st.session_state.blur_img
    
    display_n_faces.metric("Detected Faces", value = n_faces)
    display_main_img.image(label_img, caption=st.session_state.caption)

    form = step_3.form(key="selection")
    c1, c2, c3 = form.columns((1,1,1))
    
    select_lis = []
    for i, face_img in enumerate(faces_img,0):
        face_img = face_img.resize((150,150))
        if i%3==0:
            c1.image(face_img)
            select = c1.checkbox('Select', value=False, key=f'person_{i}')
            c1.markdown('---')
        elif i%3==1:
            c2.image(face_img)
            select = c2.checkbox('Select', value=False, key=f'person_{i}')
            c2.markdown('---')
        else:
            c3.image(face_img)
            select = c3.checkbox('Select', value=False, key=f'person_{i}')
            c3.markdown('---')

        select_lis.append((select,face_img))
    
    submitted = form.form_submit_button(label="Submit")

    with st.sidebar:
        st.subheader('Blur config')
        ksize = st.slider(
            "Kernel size",
            min_value=11,
            max_value= 99,
            value=29,
            step=2
            )
        st.caption('Click "Submit" button for apply config values')

    if submitted:
        blur_img = get_blur_img(img, boxes, select_lis, ksize)
        st.session_state.blur_img = blur_img
        blur_img.save(BLUR_IMG_PATH)
        st.session_state.state = 'download'
    
if st.session_state.state=='download':
    step_4.image(st.session_state.blur_img)

    with open(BLUR_IMG_PATH, 'rb') as file:
        btn = step_4.download_button(
                    label="Download image",
                    data=file,
                    file_name="Blur_image.jpg",
                    mime="image/png"
                )
        if btn:
            step_4.success('Download Success')


footer()



        

        






    