from glob import glob
from ultralytics import YOLO
import cv2
import time
import os
import streamlit as st


def save_video(video) -> None:
    cap = cv2.VideoCapture(video)
    frame = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame.append(frame)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter('./data/face_detection/tmp_video.mp4',fourcc,30,(200,200))
    for f in frame:
        writer.write(f)
    writer.release()
    cap.release()

def predict_img(path):
    model = YOLO('./model/yolov8n.pt')
    img = cv2.imread(path)
    
    results = model.predict(source=img)
    for result in results:
        result = result.numpy()
        for box,conf in zip(result.boxes.xyxy,result.boxes.conf):
            # print(box,conf)
            box = [int(num) for num in box]
            x1,y1,x2,y2 = box
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),5)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    st.image(img,caption='This is the results', width=300)

def app():

    input_choice = st.selectbox(
            'Input',
                ["Example Video",
                "Upload Your Video",
                'Youtube Link'
                ]
            )

    with st.sidebar:
        st.markdown('---')
        st.markdown(':stuck_out_tongue:')
        st.header('Config Model')
        model_dir='./model'
        model_path = st.selectbox(
            'Model Weight',
                [model.split('/')[-1] for model in glob(model_dir+'/*')]
            )
        model = YOLO(os.path.join(model_dir,model_path))

    st.title("Computer Vision Project")

    if input_choice=='Example Video':
        st.header('Example Video')
        video_path = "./data/face_detection/video3.mp4"
        video = cv2.VideoCapture(video_path)

    elif input_choice=='Upload Your Video':
        video = st.file_uploader('Upload your video',type=['mp4'])
        


    elif input_choice=='Youtube Link':
        link = st.text_input("Youtube link here")
    
    c1,c2 = st.columns((1,1))
    with c1:
        if video:
            st.video(video_path)
            st.success("Ready to Run Object Detection!")
            if st.button("Run Object Detection"):
                with st.spinner('Wait for Processing...'):
                    # results = model.predict(
                    #     video_path,
                    #     save=True,
                    #     save_txt=True,
                    #     project='./data/face_detection',
                    #     name='output',
                    #     exist_ok=True
                    #     )
                    time.sleep(2)
                st.success("Process Complete!")
                time.sleep(2)
                if os.path.exists('./data/face_detection/output/video3.mp4'):
                    st.video("data/face_detection/output/video3.mp4")
    with c2:
        if os.path.exists('./data/face_detection/output/video3.mp4'):
            st.video("data/face_detection/output/video3.mp4")
            if st.button("Refresh Output"):
                pass
    if st.button("test run"):
        my_bar = st.progress(0)
        for percent_complete in range(101):
            time.sleep(0.01)
            my_bar.progress(percent_complete)
        st.success('Finish')

        
        
    


    