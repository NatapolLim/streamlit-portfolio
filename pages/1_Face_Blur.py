from utils.utils import change_multi_state, change_state_text, get_blur_img, footer, load_img
from utils.utils_face_recognition import PreProcessPipeline
from PIL import Image
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


st.set_page_config(
    page_title="Face Blur Project",
    page_icon="🤩"
)

EXAMPLE_IMG_PATH = "assets/face_blur/example1.jpg"
BLUR_IMG_PATH = "assets/face_blur/Blur_img.jpg"

with open("style.css", 'r') as file:
    st.markdown("<style>{}</style>".format(file.read()), unsafe_allow_html=True)

st.header("Face Blue Image")

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
    with st.expander(label='Guide info', expanded=True):
        st.markdown('''
        This app used to Blur wanted faces which are detected from Face Detection model.
        <p>
        Have <kbd>3</kbd> main steps
        <p>
        <kbd>Step1</kbd>: Upload an image or try with an example image
        <p>
        <kbd>Step2</kbd>: Processing and select wanted faces
        <p>
        <kbd>Step3</kbd>: Then hit summit buttin for blur process and click 'Download' for download
        ''', unsafe_allow_html=True)
    st.caption('You can adjust a few parameters of the model below to change the result.')
    st.subheader("Face Detect Config")
    threshold = st.slider(
        "Confidence",
        min_value=50,
        max_value= 99,
        value=80,
        step=1,
        key='FB_threshold'
        )
    min_face_size = st.slider(
        'Minimum Face Size in the Image',
        min_value=10,
        max_value=100,
        value=50,
        step=1,
        key='FB_min_face_size',
        )

file = step_1.file_uploader(
    "Upload Here", type=['jpg','png'],
    on_change=change_multi_state,
    args=((('FB_state', 'load_img'),('img_input', 'upload')),),
    key='upload_file',
    label_visibility='hidden'
    )

if st.session_state.img_input=="example":
    img = load_img(EXAMPLE_IMG_PATH)

elif st.session_state.img_input=="upload":
    if isinstance(file, UploadedFile):
        img = Image.open(file).convert('RGB')
    else:
        st.error('Please Upload Image again')
        st.stop()
        
if st.session_state.FB_state=='load_img':
    display_main_img.image(img, caption='Example Image')
    display_n_faces.metric("Detected Faces", value = 0)

step_2.button(
    'Process',
    on_click=change_state_text,
    args=('FB_state', 'select'),
    use_container_width=True
    )

def select_state() -> None:
    '''Wrap process by function for reducing memory'''
    pre_process = PreProcessPipeline(img, min_face_size=min_face_size, keep_all=True)
    boxes = pre_process.extract_face_boxes(threshold=threshold//100)
    faces_img, label_img = pre_process.extract_face_img(img, boxes)

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
    submitted = form.form_submit_button(
        label="Submit",
        on_click=change_state_text,
        args=('FB_state','select'),
        use_container_width=True)

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
    
    if st.session_state.FB_state=='select' and 'blur_img' in st.session_state:
        step_4.image(st.session_state.blur_img)
        with open(BLUR_IMG_PATH, 'rb') as file:
            btn = step_4.download_button(
                        label="Download Image",
                        data=file,
                        file_name="Blur_image.jpg",
                        mime="image/png",
                        use_container_width=True
                    )
            if btn:
                step_4.success('Download Success')

if st.session_state.FB_state=='select':
    select_state()

del img

footer()    