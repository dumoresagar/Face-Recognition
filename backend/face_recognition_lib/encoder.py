import face_recognition
import numpy as np

class FaceEncoder:
    def encode_faces(self, image):
        # Check if the input is a file path or a NumPy array
        if isinstance(image, str):
            image = face_recognition.load_image_file(image)
        elif not isinstance(image, np.ndarray):
            raise ValueError("Input image is not a valid file path or NumPy array")

        face_encodings = face_recognition.face_encodings(image)
        return face_encodings