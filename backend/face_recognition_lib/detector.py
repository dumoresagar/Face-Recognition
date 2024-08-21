# import cv2
# import numpy as np

# class FaceDetector:
#     def __init__(self, cascade_path=cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'):
#         self.face_cascade = cv2.CascadeClassifier(cascade_path)

#     def detect_faces(self, image_np):
#         if image_np is None or not isinstance(image_np, np.ndarray):
#             raise ValueError("Input image is not a valid NumPy array")

#         gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#         return faces, image_np

# from mtcnn import MTCNN
# import numpy as np
# class FaceDetector:
#     def __init__(self):
#         self.detector = MTCNN()

#     def detect_faces(self, image_np):
#         if image_np is None or not isinstance(image_np, np.ndarray):
#             raise ValueError("Input image is not a valid NumPy array")

#         # MTCNN returns a list of dicts with details like bounding box and keypoints
#         faces = self.detector.detect_faces(image_np)
        
#         # Extract bounding boxes
#         face_bboxes = [face['box'] for face in faces]
        
#         return face_bboxes, image_np

# class FaceDetector:
#     def __init__(self):
#         self.detector = MTCNN(steps_threshold=[0.6, 0.7, 0.7])  # Adjust these values as needed

#     def detect_faces(self, image_np):
#         if image_np is None or not isinstance(image_np, np.ndarray):
#             raise ValueError("Input image is not a valid NumPy array")

#         faces = self.detector.detect_faces(image_np)
#         face_bboxes = [face['box'] for face in faces]
#         return face_bboxes, image_np


#######################################################
from retinaface import RetinaFace
import numpy as np

class FaceDetector:
    def __init__(self):
        pass  # No initialization needed for RetinaFace

    def detect_faces(self, image_np):
        if image_np is None or not isinstance(image_np, np.ndarray):
            raise ValueError("Input image is not a valid NumPy array")

        # RetinaFace expects BGR format (compatible with OpenCV)
        # The function returns a dictionary with face bounding boxes and landmarks
        faces = RetinaFace.detect_faces(image_np)

        # Extract bounding boxes
        face_bboxes = []
        if isinstance(faces, dict):
            for face_key in faces.keys():
                face_bboxes.append(faces[face_key]['facial_area'])

        return face_bboxes, image_np
