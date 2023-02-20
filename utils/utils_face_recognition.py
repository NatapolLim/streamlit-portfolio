from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import cv2
import torch
import numpy as np
from utils.utils import get_faces_img, draw

class PreProcesssPipeline:
    '''Store MTCNN and model'''
    def __init__(self) -> None:
        self.mtcnn = MTCNN(
            image_size=160,
            margin=0,
            min_face_size=50,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=True,
            keep_all=False,
            device=torch.device('cpu'),
        )
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(torch.device('cpu'))
    
    def extract_face_boxes(self, img_: Image) -> list:
        '''Extract face and return coordinate xy of box'''
        batch_boxes, batch_probs, batch_points = self.mtcnn.detect(img_, landmarks=True)
        batch_boxes, _, _ = self.mtcnn.select_boxes(
            batch_boxes,
            batch_probs,
            batch_points,
            img_,
            method='probability'
            )
        return batch_boxes

    def extract_face_img(self, img_: Image) -> Image:
        '''Extract face image using MTCNN pipeline and return cropped face image'''
        batch_boxes = self.extract_face_boxes(img_)
        faces_img = get_faces_img(img_, batch_boxes)[0]
        label_face_img = draw(img_, batch_boxes, width=img_.size[0]//200)
        
        return faces_img, label_face_img

    def encode_face(self, img_: Image)-> torch.Tensor:
        '''Process face cropped to face features.'''
        batch_boxes = self.extract_face_boxes(img_)
        face_ = self.mtcnn.extract(img_, batch_boxes, save_path=None)
        face_features_ = self.model(face_.unsqueeze(0)).detach()
        return face_features_