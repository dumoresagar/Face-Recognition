import face_recognition


class FaceRecognizer:
    def __init__(self, known_encodings, known_names):
        self.known_encodings = known_encodings
        self.known_names = known_names

    def recognize_faces(self, face_encodings):
        results = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            name = "Not Match"
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_names[first_match_index]
            results.append(name)
        return results