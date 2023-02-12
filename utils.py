# from facenet_pytorch import MTCNN
# from PIL import Image, ImageDraw
# from IPython import display
# import pandas as pd
# import numpy as np
# import torch
import cv2
# import os

#Face Blur
def resize_box(ori_img_size,boxes, margin=0):
    new_boxes=[]
    for box in boxes:
        box = [
            int(max(box[0]-margin/2,0)),
            int(max(box[1]-margin/2,0)),
            int(min(box[2]+margin/2, ori_img_size[1])),
            int(min(box[3]+margin/2, ori_img_size[0])),
        ]
        new_boxes.append(box)
    return new_boxes

def gauss_blur_face(box, img, size):
    x1, y1, x2, y2 = box
    roi = img[y1:y2, x1:x2]
    roi = cv2.GaussianBlur(roi, (size, size), 30)
    img[y1:y2, x1:x2] = roi
    return img

# #Not use
# TEMP_FILES_DIR = "data/face_recognition/temp"
# UPLOAD_IMG_PATH = "data/face_recognition/temp/tmp_img.jpg"
# EXAMPLE_IMG_PATH = "data/face_recognition/example1.jpg"
# FACES_IMG_PATH = "data/face_recognition/temp/faces_output/face.jpg"
# FACES_IMG_DIR = "data/face_recognition/temp/faces_output"
# BOXES_POINTS_DIR = "data/face_recognition/temp/face_boxes"

# class FaceRec():
#     def __init__(self, img_path) -> None:
#         self.device = torch.device('cpu')
#         self.img_path = img_path
#         self.img = get_img(img_path)
#         self.width, self.height = self.img.size
#         self.detect_faces_img = self.img.copy()
#         self.blur_img = self.img.copy()

#         # self.resnet =InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
#         self.n_face = 0
#         self.face_paths = []
#         self.batch_boxes = None
#         self.faces = None
#         self.boxes_info = {}

#     def cropped_face(self):
#         # delete_tmp_files_if_exist(FACES_IMG_DIR)
#         # delete_tmp_files_if_exist(BOXES_POINTS_DIR)
#         delete_tmp_files_if_exist(TEMP_FILES_DIR)
#         mtcnn = MTCNN(
#             image_size=160,
#             margin=20,
#             min_face_size=100,
#             thresholds=[0.6, 0.7, 0.7],
#             factor=0.709,
#             post_process=True,
#             keep_all=True,
#             device=self.device
#         )
#         self.batch_boxes, batch_probs, batch_points = mtcnn.detect(self.img, landmarks=True)
#         self.faces= mtcnn.extract(self.img, self.batch_boxes, FACES_IMG_PATH)
#         self.n_face = self.faces.shape[0]

#         self.detect_faces_img = self.img.copy()
#         draw = ImageDraw.Draw(self.detect_faces_img)
#         for box in self.batch_boxes:
#             draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
        
#         self.blur_img.save(os.path.join(TEMP_FILES_DIR,'blur_img.jpg'))
#         self.detect_faces_img.save(os.path.join(TEMP_FILES_DIR,'labels.jpg'))
#         self.save_boxes(self.batch_boxes)
#         self.save_n_faces()

#         return self.detect_faces_img

#     def save_boxes(self, batch_boxes):
#         with open(os.path.join(TEMP_FILES_DIR, 'boxes.txt'), 'w') as file:
#             for box in batch_boxes:
#                 for point in box:
#                     file.write(str(int(point)))
#                     file.write(" ")
#                 file.write('\n')

#     def save_n_faces(self):
#         with open(os.path.join(TEMP_FILES_DIR,'n_faces.txt'), 'w') as file:
#             file.write(str(self.n_face))

#     def inference():
#         pass

# def get_img(path):
#     img = cv2.imread(path)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = Image.fromarray(img)
#     return img

# def delete_tmp_files_if_exist(path_dir):
#     output_files = os.listdir(path_dir)
#     # print(output_files)
#     if len(output_files)!=0:
#         for file in output_files:
#             if file =='faces_output':
#                 delete_tmp_files_if_exist(FACES_IMG_DIR)
#             else:    
#                 os.remove(os.path.join(path_dir, file))

# def blur_face(xyxy, img_array):
#     x1,y1,x2,y2 = [int(point) for point in xyxy]
#     roi = img_array[y1:y2,x1:x2]
#     roi = cv2.GaussianBlur(roi, (29, 29), 30)
#     img_array[y1:y2, x1:x2] = roi
#     blur_img = Image.fromarray(img_array)
#     blur_img.save(os.path.join(TEMP_FILES_DIR,'blur_img.jpg'))
#     return blur_img

# class FaceBox():
#     def __init__(self, img, filename) -> None:
#         self.img = img
#         self.xyxy = None
#         self.encode = None
#         self.select = False
#         self.name = "Unknown"
#         self.filename = filename