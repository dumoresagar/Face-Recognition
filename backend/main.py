import os
import json
from face_recognition_lib.detector import FaceDetector
from face_recognition_lib.encoder import FaceEncoder
from face_recognition_lib.recognizer import FaceRecognizer

def load_known_faces(directory):
    known_encodings = []
    known_names = []
    encoder = FaceEncoder()
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            name = os.path.splitext(filename)[0]
            face_encodings = encoder.encode_faces(image_path)
            if face_encodings:
                known_encodings.append(face_encodings[0])
                known_names.append(name)
    return known_encodings, known_names

def recognize_from_image(image_path, known_faces_dir):
    known_encodings, known_names = load_known_faces(known_faces_dir)
    detector = FaceDetector()
    encoder = FaceEncoder()
    recognizer = FaceRecognizer(known_encodings, known_names)

    faces, _ = detector.detect_faces(image_path)
    face_encodings = encoder.encode_faces(image_path)
    results = recognizer.recognize_faces(face_encodings)

    response = {'data': []}
    for result in results:
        response['data'].append(result)

    # Print the response in JSON format
    print(json.dumps(response, indent=4))

if __name__ == "__main__":
    test_image_path = "data/test_image.jpg"
    known_faces_dir = "data/known_faces"
    recognize_from_image(test_image_path, known_faces_dir)
