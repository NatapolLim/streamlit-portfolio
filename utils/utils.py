import os
import base64
import time
import numpy as np
import pandas as pd
from typing import Tuple, List
import cv2
from PIL import Image, ImageDraw
from PIL.JpegImagePlugin import JpegImageFile
import streamlit as st
from streamlit.components.v1 import html
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1

#State control for Streamlit
def change_multi_state(state_pair: tuple) -> None:
    '''Change State from callback fucntion follow the state input.'''
    for state_key, state in state_pair:
        if 'FR_img_input' == state_key and state.startswith('webcam'):
            backup_img(state)
        st.session_state[state_key] = state

def change_state_text(state_key: str, state: str) -> None:
    '''Change State from callback fucntion follow the state input.'''
    st.session_state[state_key] = state

def change_state_bool(state_key: str,state: bool) -> None:
    '''Change State from callback fucntion follow the state input.'''
    st.session_state[state_key] = state

def backup_img(key: str) -> None:
    '''Backup image from webcam and Check in case webcam is closed, then do not backup again.'''
    if st.session_state[key] is not None:
        _img = st.session_state[key]
        st.session_state.backup_img = Image.open(_img).copy()

#Profile Page
def nav_page(page_name, timeout_secs=3) -> None:
    '''Function for navigation to another page'''
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

def txt(a: str, b: str) -> None:
    '''Display text in specific pattern.'''
    _, col1, col2 = st.columns((0.1,4, 1))
    with col1:
        st.markdown(a, unsafe_allow_html=True)
    with col2:
        st.markdown(b, unsafe_allow_html=True)

def txt_skills(topic: str, skills: str) -> None:
    '''Display text in specific pattern.'''
    _, col1, col2 = st.columns((0.1, 1, 3))
    with col1:
        st.markdown(topic)
    with col2:
        text=""""""
        for skill in skills:
            text+=f"<kbd>{skill}</kbd>"
            text+=', '
        st.markdown(text[:-2], unsafe_allow_html=True)

#Face fucn model
@st.cache_resource
def call_mtcnn(min_face_size: int=50, keep_all: bool=False) -> MTCNN:
    '''create instance mtcnn'''
    mtcnn = MTCNN(
        image_size=160,
        margin=0,
        min_face_size=min_face_size,
        thresholds=[0.6, 0.7, 0.7],
        factor=0.709,
        post_process=True,
        keep_all=keep_all,
        device=torch.device('cpu'),
    )
    return mtcnn

@st.cache_resource
def call_facemodel() -> InceptionResnetV1:
    '''create instance model'''
    model = InceptionResnetV1(pretrained='vggface2').eval().to(torch.device('cpu'))
    return model

def adjust_boxes(ori_img_size: Tuple[int,int], boxes: List, margin: int=0) -> List:
    '''Resize boxes to proper format.'''
    new_boxes=[]
    for box in boxes:
        box = [
            int(max(box[0]-margin/2,0)),
            int(max(box[1]-margin/2,0)),
            int(min(box[2]+margin/2, ori_img_size[0])),
            int(min(box[3]+margin/2, ori_img_size[1])),
        ]
        new_boxes.append(box)
    return new_boxes

def get_faces_img(img: JpegImageFile ,boxes: List, img_size: tuple=(160,160)) -> List:
    '''Extract faces form image using given boxes point'''
    faces_img = []
    img = np.array(img)
    for box in boxes:
        face = img[box[1]:box[3] ,box[0]:box[2]]
        face = cv2.resize(
            face,
            img_size,
            interpolation=cv2.INTER_AREA
            ).copy()
        faces_img.append(Image.fromarray(face))
    return faces_img

def draw(img: JpegImageFile, boxes: List, width: int=6) -> JpegImageFile:
    '''Draw regtangle box in the image'''
    label_img = img.copy()
    draw_ = ImageDraw.Draw(label_img)
    for box in boxes:
        draw_.rectangle(box, outline=(255, 0, 0), width = width)
    return label_img

#Face Blur
def gauss_blur_face(box: List, img: JpegImageFile, size: int) -> JpegImageFile:
    '''Blur area in rectangle boxes.'''
    roi = img[box[1]:box[3], box[0]:box[2]]
    roi = cv2.GaussianBlur(roi, (size, size), 30)
    img[box[1]:box[3], box[0]:box[2]] = roi
    return img

def get_blur_img(img_: JpegImageFile, boxes_: List, select_lis_: List[bool], ksize_: int) -> JpegImageFile:
    '''Blur faces image as boxes input'''
    img_ = np.array(img_)
    boxes_ = adjust_boxes(img_.shape, boxes_, margin=20)
    for (selected, _), box in zip(select_lis_, boxes_):
        if not selected:
            continue
        else:
            img_ = gauss_blur_face(box, img_, ksize_)
    return Image.fromarray(img_)

#Face_blur_video
@st.cache_resource
def process(_mtcnn,img, threshold=0.9):
    batch_boxes, batch_probs, _ = _mtcnn.detect(img, landmarks=True)
    if batch_boxes is None:
        return [], []
    boxes=[]
    probs=[]
    for box, prob in zip(batch_boxes, batch_probs):
        if prob < threshold:
            continue
        else:
            box = [int(p) for p in box]
            boxes.append(box)
            probs.append(prob)

    return probs, boxes

#General
@st.cache_data
def load_img(path: str) -> JpegImageFile:
    time.sleep(1)
    return Image.open(path)

@st.cache_data
def load_df(path: str) -> pd.DataFrame:
    time.sleep(1)
    return pd.read_csv(path, index_col=None)

def to_bin(img_path) -> bytes:
    '''Read image as binary'''
    with open(img_path, "rb") as file:
        txt_ = file.read()
        bin_ = base64.b64encode(txt_).decode("utf-8")
    return bin_

def html_display_img_with_href(img_path: str, target_url: str, size=30) -> str:
    '''generate html code for display tagged image link'''
    img_format = os.path.splitext(img_path)[-1].replace('.', '')
    bin_str = to_bin(img_path)
    html_code = f'''
        <a href="{target_url}">
            <img class="center" src="data:image/{img_format};base64,{bin_str}" width="{size}" height="{size}"/>
        </a>'''
    return html_code

def footer() -> None:
    '''Show footer in every pages'''
    st.markdown("""<hr class="style1">""", unsafe_allow_html=True)
    st.markdown('''#### Contact''')
    _, c2 ,c3, _ = st.columns((3,1,1,3))
    linkedin_img_html = html_display_img_with_href(
        'assets/profile/640px-LinkedIn_logo_initials.png',
        'https://www.linkedin.com/in/natapol-limpananuwat-686595202'
        )
    c2.write(linkedin_img_html, unsafe_allow_html=True)

    github_img_html = html_display_img_with_href(
        'assets/profile/1164606_telegram-icon-github-icon-png-white-png-download.png-removebg-preview.png',
        'https://github.com/NatapolLim'
        )
    c3.write(github_img_html, unsafe_allow_html=True)

    _, c2 ,_ = st.columns((1,3,1))
    c2.markdown("""<address>
    Address: Bangkoknoi Bangkok 10700</br>
    Email: <a href="mailto:natapolllim@gmail.com">Natapolllim@gmail.com</a></br>
    Tel: 084-926-7299
    </address>
    """, unsafe_allow_html=True)
