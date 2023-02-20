from streamlit.components.v1 import html
import streamlit as st
from PIL import Image, ImageDraw
import base64
import cv2
import os
import numpy as np

#Profile Page
def nav_page(page_name, timeout_secs=3):
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

def txt(a, b):
    _, col1, col2 = st.columns((0.1,4, 1))
    with col1:
        st.markdown(a, unsafe_allow_html=True)
    with col2:
        st.markdown(b, unsafe_allow_html=True)

def txt_skills(topic, skills):
    _, col1, col2 = st.columns((0.1, 1, 3))
    with col1:
        st.markdown(topic)
    with col2:
        text=""""""
        for skill in skills:
            text+=f"<kbd>{skill}</kbd>"
            text+=', '
        
        st.markdown(text[:-2], unsafe_allow_html=True)

#Face Blur
def adjust_boxes(ori_img_size: tuple,boxes: list, margin: int=0) -> list:
    '''Resize boxes to proper format'''
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

def gauss_blur_face(box, img, size):
    x1, y1, x2, y2 = box
    roi = img[y1:y2, x1:x2]
    roi = cv2.GaussianBlur(roi, (size, size), 30)
    img[y1:y2, x1:x2] = roi
    return img

def to_bin(img_path):
    with open(img_path, "rb") as file:
        contents = file.read()
        bin = base64.b64encode(contents).decode("utf-8")
    return bin

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

#Face Recognition
def get_faces_img(img: Image ,boxes: list, img_size: tuple=(160,160)) -> list:
    '''Extract faces form image using given boxes point'''
    faces_img = []
    original_img_size=img.size
    img = np.array(img)
    boxes = adjust_boxes(original_img_size, boxes)
    for box in boxes:
        face = img[box[1]:box[3] ,box[0]:box[2]]
        face = cv2.resize(
            face,
            img_size,
            interpolation=cv2.INTER_AREA
            ).copy()
        faces_img.append(Image.fromarray(face))
    return faces_img


def draw(img: Image, boxes: list, width: int=6) -> Image:
    '''Draw regtangle box in the image'''
    label_img = img.copy()
    draw = ImageDraw.Draw(label_img)
    for box in boxes:
        draw.rectangle(box, outline=(255, 0, 0), width = width)

    return label_img


#General
def html_display_img_with_href(img_path, target_url, size=30):
    img_format = os.path.splitext(img_path)[-1].replace('.', '')
    bin_str = to_bin(img_path)
    html_code = f'''
        <a href="{target_url}">
            <img class="center" src="data:image/{img_format};base64,{bin_str}" width="{size}" height="{size}"/>
        </a>'''
    return html_code

def footer():
    st.markdown("""<hr class="style1">""", unsafe_allow_html=True)
    st.markdown('''#### Contact''')
    _, c2 ,c3, _ = st.columns((3,1,1,3))

    linkedin_img_html = html_display_img_with_href(
        'images/profile/640px-LinkedIn_logo_initials.png',
        'https://www.linkedin.com/in/natapol-limpananuwat-686595202'
        )
    c2.write(linkedin_img_html, unsafe_allow_html=True)

    github_img_html = html_display_img_with_href(
        'images/profile/1164606_telegram-icon-github-icon-png-white-png-download.png-removebg-preview.png',
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
