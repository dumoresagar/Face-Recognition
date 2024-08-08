import cv2
import numpy as np

class FaceDetector:
    def __init__(self, cascade_path=cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'):
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def detect_faces(self, image_np):
        if image_np is None or not isinstance(image_np, np.ndarray):
            raise ValueError("Input image is not a valid NumPy array")

        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces, image_np
