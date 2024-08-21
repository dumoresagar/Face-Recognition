from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
import cv2
import numpy as np
import os
from io import BytesIO
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from PIL import Image
import face_recognition
from face_recognition_lib.detector import FaceDetector
from face_recognition_lib.encoder import FaceEncoder
from face_recognition_lib.recognizer import FaceRecognizer
from .serializer import FaceRecognitionSerializer

# Define the path to known faces in the media directory
# KNOWN_FACES_DIR = os.path.join(settings.MEDIA_ROOT, 'data/known_faces')
class ProtoTypeLookUp(GenericAPIView):

    def get(self, request, *args, **kwargs):
        return Response({'key': 'all-set'}, status=http_status.HTTP_200_OK)




def load_known_faces(directory):
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist")

    known_encodings = []
    known_names = []
    encoder = FaceEncoder()
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image_path = os.path.join(directory, filename)
            name = os.path.splitext(filename)[0]
            face_encodings = encoder.encode_faces(image_path)
            if face_encodings:
                known_encodings.append(face_encodings[0])
                known_names.append(name)
    return known_encodings, known_names

def recognize_from_image(image_np, known_faces_dir):
    known_encodings, known_names = load_known_faces(known_faces_dir)
    detector = FaceDetector()
    encoder = FaceEncoder()
    recognizer = FaceRecognizer(known_encodings, known_names)

    # Convert to BGR format for OpenCV if needed
    if image_np.ndim == 3 and image_np.shape[2] == 4:  # RGBA format
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
    elif image_np.ndim == 3 and image_np.shape[2] == 1:  # Grayscale format
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)

    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    faces, _ = detector.detect_faces(image_cv)
    if len(faces) == 0:
        return ["No face detected"]

    face_encodings = encoder.encode_faces(image_cv)
    results = recognizer.recognize_faces(face_encodings)

    return results


class RecognizeFaceAPIView(APIView):
    permission_classes = [AllowAny]  # Adjust permissions as needed
    authentication_classes = (TokenAuthentication,)  # Adjust authentication as needed

    def post(self, request, *args, **kwargs):
        serializer = FaceRecognitionSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']

            try:
                # Read the uploaded image file into a PIL image
                image = Image.open(BytesIO(image_file.read()))

                # Convert the PIL image to a NumPy array
                image_np = np.array(image)

                # Perform recognition
                results = recognize_from_image(image_np, os.path.join(settings.MEDIA_ROOT, 'data/known_faces'))

                if results and results[0] != "No face detected":
                    matched_name = results[0]
                    image_url = os.path.join(settings.MEDIA_URL, 'data/known_faces', f'{matched_name}.jpg')

                    response = {
                        'data': matched_name,  # Return the first result (name of the matched person)
                        'image_url': request.build_absolute_uri(image_url)  # Absolute URL of the matched image
                    }
                else:
                    response = {'data': 'Not match'}

                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)