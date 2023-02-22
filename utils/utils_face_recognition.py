'''Group nescessary pipeline which implement'''
import os
import pandas as pd
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import PIL
import torch
import numpy as np
from utils.utils import get_faces_img, draw
import streamlit as st

DATA_STORE_DIR = "assets/face_recognition/data_store"
class PreProcesssPipeline:
    '''Store MTCNN and model and perform extracting faces'''
    def __init__(self, min_face_size: int=50, keep_all: bool=False) -> None:
        self.mtcnn = MTCNN(
            image_size=160,
            margin=0,
            min_face_size=min_face_size,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=True,
            keep_all=keep_all,
            device=torch.device('cpu'),
        )
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(torch.device('cpu'))
        self.keep_all = keep_all
    
    def extract_face_boxes(self, img_: Image, threshold: float=0.9) -> list:
        '''Extract face and return coordinate xy of box'''
        batch_boxes, batch_probs, batch_points = self.mtcnn.detect(img_, landmarks=True)
        if not self.keep_all:
            batch_boxes, _, _ = self.mtcnn.select_boxes(
                batch_boxes,
                batch_probs,
                batch_points,
                img_,
                method='probability'
                )
        return batch_boxes

    def extract_face_img(self, img_: Image,  threshold: float=0.9) -> Image:
        '''Extract face image using MTCNN pipeline and return cropped face image'''
        batch_boxes = self.extract_face_boxes(img_, threshold)
        if batch_boxes is None:
            return None, None
        faces_img = get_faces_img(img_, batch_boxes)
        label_face_img = draw(img_, batch_boxes, width=img_.size[0]//200)
        return faces_img, label_face_img

    def encode_face(self, img_: Image)-> torch.Tensor:
        '''Process face cropped to face features.'''
        batch_boxes = self.extract_face_boxes(img_)
        face_ = self.mtcnn.extract(img_, batch_boxes, save_path=None)
        face_features_ = self.model(face_.unsqueeze(0)).detach()
        return face_features_

class CompareFacesPipeline:
    '''For compare faces pipeline and manipulate dataframe.'''
    def __init__(self, face_features_: torch.Tensor) -> None:
        self.face_features = face_features_
        self.all_faces = pd.read_csv(
            os.path.join(DATA_STORE_DIR, 'data_map/data_map.csv'),
            index_col=None
            )

    @st.cache_data
    def load_tensors(faces_df: pd.DataFrame) -> torch.Tensor:
        '''Cache loading tensor from db'''
        faces_features_in_db=[]
        filenames_all_faces = faces_df['filename']
        for file_ in filenames_all_faces:
            face_features_in_db = torch.load(file_)
            faces_features_in_db.append(face_features_in_db)
        return faces_features_in_db

    def cal_euclidience_dis(self, face_features_: torch.Tensor) -> list:
        '''Compare and calculate the euclidence distance between specific faces.'''
        dists_=[]
        faces_features_in_db = self.load_tensors(self.all_faces)
        for face_features_in_db in faces_features_in_db:
            dist = (face_features_-face_features_in_db).norm().item()
            dists_.append(dist)
        return dists_

    def compare_faces(self, face_features_: torch.Tensor, threshold: float=0.6, return_dist: bool=False) -> int:
        '''Return index that the most similar and check condition
        which distance must under threshold.'''
        dists_ = self.cal_euclidience_dis(face_features_)
        idx_ = np.argmin(dists_)
        if dists_[idx_] < threshold:
            ret_ = idx_
        else:
            ret_ = -1 # No one similar to the input face
        if return_dist:
            return ret_, dists_[ret_]
        return ret_

    @st.cache_data
    def get_info(face_df, idx_: int) -> list:
        '''Gather data form Dataframe and the picture of the most similar person.'''
        if idx_ == -1:
            return 0, 'Unknown', 'Unknown'
        row_ = face_df.iloc[[idx_]]
        picture_file = row_['filename'].values[0].split('/')[-1].split('.')[0]
        name_ = row_['name'].values[0]
        picture_ = Image.open(os.path.join(DATA_STORE_DIR, 'pictures', picture_file+'.jpg'))
        return 1, name_, picture_

    def fetch_data_form_db(self, idx_: int) -> list:
        '''Recieve index of database and get data info of that face.'''
        pass