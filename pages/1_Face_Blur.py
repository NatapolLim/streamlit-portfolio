from utils.utils import change_multi_state, change_state_text, get_blur_img, footer
from utils.utils_face_recognition import PreProcesssPipeline
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Face Blur Project",
    page_icon="🤩"
)

EXAMPLE_IMG_PATH = "assets/face_blur/example1.jpg"
BLUR_IMG_PATH = "assets/face_blur/Blur_img.jpg"

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

st.header("Face Blue Image")

# if choose == 'Image':
if 'FB_state' not in st.session_state:
    st.session_state.FB_state = 'load_img'
    st.session_state.img_input = 'example'

#layout  
step_1 = st.expander("Upload Your Image", expanded = False)
step_2 = st.expander("Detected Face Output", expanded = True)
step_3 = st.expander("Select Faces to Blur", expanded = True)
step_4 = st.expander("Blured Image", expanded = True)

col1, col2 = step_2.columns((3,1))
display_main_img = col1.empty()
display_n_faces = col2.empty()

with st.sidebar:
    st.subheader("Face Detect Config")
    threshold = st.slider(
        "Confidence",
        min_value=50,
        max_value= 99,
        value=80,
        step=1
        )
    min_face_size = st.slider(
        'Minimum Face Size in the Image',
        min_value=10,
        max_value=100,
        value=50,
        step=1
        )
    st.caption('Click "Process" button for apply config values')

file = step_1.file_uploader(
    "", type=['jpg','png'],
    on_change=change_multi_state,
    args=((('FB_state', 'load_img'),('img_input', 'upload')),),
    key='upload_file'
    )

if st.session_state.img_input=="example":
    img = Image.open(EXAMPLE_IMG_PATH)

elif st.session_state.img_input=="upload":
    if isinstance(file, type(None)):
        st.error('Please Upload Image again')
        st.stop()
    else:
        img = Image.open(file)

if st.session_state.FB_state=='load_img':
    display_main_img.image(img, caption='Example Image')
    display_n_faces.metric("Detected Faces", value = 0)

step_2.button(
    'Process',
    on_click=change_state_text,
    args=('FB_state', 'select')
    )

if st.session_state.FB_state=='select':
    pre_process = PreProcesssPipeline(min_face_size=min_face_size, keep_all=True)
    faces_img, label_img = pre_process.extract_face_img(img, threshold//100)

    if faces_img is not None:
        display_main_img.image(label_img, caption='Labeled Image')
        display_n_faces.metric("Detected Faces", value = len(faces_img))
    else:
        st.error('Image have no face!, please upload new Image')

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
    submitted = form.form_submit_button(label="Submit", on_click=change_state_text, args=('FB_state','select'))

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
        boxes = pre_process.extract_face_boxes(img, threshold)
        blur_img = get_blur_img(img, boxes, select_lis, ksize)
        st.session_state.blur_img = blur_img
        blur_img.save(BLUR_IMG_PATH)
    
if st.session_state.FB_state=='select' and 'blur_img' in st.session_state:
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