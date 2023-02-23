'''Group nescessary pipeline which implement'''
import os
import pandas as pd
from PIL import Image
import torch
import numpy as np
from utils.utils import get_faces_img, draw, call_mtcnn, call_facemodel, adjust_boxes
import streamlit as st
from typing import Optional, List, Tuple
from PIL.JpegImagePlugin import JpegImageFile


DATA_STORE_DIR = "assets/face_recognition/data_store"

class PreProcessPipeline:
    '''Call model and build pipeline for pre-process image.'''
    def __init__(self, img_, min_face_size: int=50, keep_all: bool=False) -> None:
        self.mtcnn = call_mtcnn(min_face_size, keep_all)
        self.face_model = call_facemodel()
        self.img = img_
        self.keep_all = keep_all

    def extract_face_boxes(self, threshold: float=0.9) -> List:
        '''Extract face and return coordinate xy of box'''
        mtcnn = self.mtcnn
        batch_boxes, batch_probs, batch_points = mtcnn.detect(self.img, landmarks=True)
        if not self.keep_all:
            batch_boxes, batch_probs, batch_points = mtcnn.select_boxes(
                batch_boxes,
                batch_probs,
                batch_points,
                self.img,
                method='probability'
                )
            batch_boxes = batch_boxes[0]
        batch_boxes = batch_boxes[batch_probs>threshold]
        batch_boxes = adjust_boxes(self.img.size, batch_boxes)
        if batch_boxes is None or not batch_boxes:
            st.error('Image has no face, please upload another image.')
            st.stop()
        return batch_boxes

    @staticmethod
    def extract_face_img(img_: JpegImageFile, batch_boxes: List) -> Tuple[List, JpegImageFile]:
        '''Extract face image using MTCNN pipeline and return cropped face image'''
        faces_img = get_faces_img(img_, batch_boxes)
        label_face_img = draw(img_, batch_boxes, width=img_.size[0]//200)
        return faces_img, label_face_img


    def encode_face(self, batch_boxes: List)-> torch.Tensor:
        '''Process face cropped to face features.'''
        mtcnn = self.mtcnn
        model = self.face_model
        batch_boxes = np.array(batch_boxes, dtype=int)
        face_ = mtcnn.extract(self.img, batch_boxes, save_path=None)
        face_features_ = model(face_.unsqueeze(0)).detach()
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

    def cal_euclidience_dis(self, face_features_: torch.Tensor) -> List:
        '''Compare and calculate the euclidence distance between specific faces.'''
        dists_=[]
        faces_features_in_db = self.load_tensors(self.all_faces)
        for face_features_in_db in faces_features_in_db:
            dist = (face_features_-face_features_in_db).norm().item()
            dists_.append(dist)
        return dists_

    def compare_faces(self, face_features_: torch.Tensor, threshold: float=0.6, return_dist: bool=False) -> Optional[int]:
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

    @staticmethod
    def get_info(face_df, idx_: int) -> Tuple[int, str, JpegImageFile]:
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