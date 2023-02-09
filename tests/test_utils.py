import numpy as np
import pytest
import cv2
import sys
 
# setting path
sys.path.append('../streamlit-portfolio')

def test_gauss_blur_face():
    from utils import gauss_blur_face
    #testing input
    box = [30,100,50,200]
    img=cv2.imread("src/face_blur/example1.jpg")
    size=29
    x1, y1, x2, y2 = box
    result = gauss_blur_face(box, img, size)

    assert np.all(result[y1:y2, x1:x2]) == np.all(cv2.GaussianBlur(img[y1:y2, x1:x2], (size, size), 30)), f'Expected Blur inside the box'
    assert result.shape == img.shape, f'Expected image shape {img.shape}, but got {result.shape}'
    assert isinstance(result, np.ndarray)

def test_resize_box():
    from utils import resize_box

    ori_img_size = (200, 300)
    boxes = [[50, 50, 100, 100], [150, 150, 500, 200]]
    margin = 0
    new_boxes = resize_box(ori_img_size, boxes, margin)

    # Test case 1
    assert len(new_boxes) == len(boxes), f"Expected {len(boxes)}, but got {len(new_boxes)}"
    # Test case 2
    for box in new_boxes:
        x1, y1, x2, y2 = box
        assert 0 <= x1 < x2 <= ori_img_size[1], f"x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2}"
        assert 0 <= y1 < y2 <= ori_img_size[0], f"x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2}"

    # Test case 3
    boxes = [[50, 50, 100, 100]]
    margin = 20
    new_boxes = resize_box(ori_img_size, boxes, margin)
    x1, y1, x2, y2 = new_boxes[0]
    assert x2 - x1 == 70, f"Expected 120, but got {x2 - x1}"
    assert y2 - y1 == 70, f"Expected 120, but got {y2 - y1}"

    # Test case 4
    boxes = []
    margin = 20
    new_boxes = resize_box(ori_img_size, boxes, margin)
    assert len(new_boxes) == 0, f"Expected 0, but got {len(new_boxes)}"

    
    # Test case 5
    boxes = [[0, 50, 1000, 100]]
    margin = 20
    new_boxes = resize_box(ori_img_size, boxes, margin)
    expected_boxes = [[0, 40, 300, 110]]
    assert new_boxes == expected_boxes, f"Expected {expected_boxes}, but got {new_boxes}"

if __name__=="__main__":
    pass