from rest_framework.generics import GenericAPIView,RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_auth.views import (LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView,)
from users.models import User,Role
from restfull_apis.version_0.permissions.guest import IsTrustedGuest
from .serializer import (
    RegisterSerializer, UserDetailSerializer, CustomPasswordChangeSerializer,
    CustomPasswordResetSerializer, CustomPasswordResetConfirmSerializer,UpdateUserSerializer,
)
from rest_framework import status
from rest_framework.views import APIView
from users.models import Role

class ProtoTypeLookUp(GenericAPIView):

    def get(self, request, *args, **kwargs):
        return Response({'key': 'all-set'}, status=http_status.HTTP_200_OK)


class CustomLoginAPIView(LoginView):

    """
    <h1 id="api_title">Login API</h1>
    <p id="api_details">API accepts username and password as input and returns user token as a response.</p>
    <pre>
    <code>
        API Method : POST
        Token Type : Guest Token ==> GUEST-AUTH-TOKEN : {token_provided_by_developer}
        </code>
    </pre>
    <p id="api_response_title"><strong>Parameters</strong></p>
    <pre>
        <code>
        {
            "username_or_email": "CharField",  # Users name
            "password": "CharField"  # Users password (required)
        }
        </code>
    </pre>
    <p id="api_response_title"><strong>Response</strong></p>
    <pre>
        <code>
        {
            "key": "CharField",  # users access/auth token
        }
        </code>
    </pre>
    <p id="api_response_title"><strong>API Status</strong></p>
    <pre>
        <code>
        <span>200 : Login success.</span>
        <span>400 : Data validation error.</span>
        <span>500 : Internal server error.</span>
        </code>
    </pre>
    """

    authentication_classes = ()
    permission_classes = (IsTrustedGuest,)


class RegisterAPIView(GenericAPIView):

    """
    <h1 id="api_title">Register Users API</h1>
    <p id="api_details">API register users using email, username and password.</p>
    <pre>
        <code>
            API Method : POST
            Token Type : Guest Token ==> GUEST-AUTH-TOKEN : {token_provided_by_developer}
        </code>
    </pre>
    <p id="api_response_title"><strong>Parameters</strong></p>
    <pre>
        <code>
           {
               "username": "CharField",  # Username (required)
               "email": "EmailField",  # Email (required)
               "password": "CharField"  # Password (required)
           }
       </code>
   </pre>
    <p id="api_response_title"><strong>Response</strong></p>
    <pre>
        <code>
            {
                "id": "IntField",
                "username": "CharField",
                "email": "CharField",
                "is_active": "BooleanField"
            }
        </code>
    </pre>
    <p id="api_response_title"><strong>API Status</strong></p>
    <pre>
        <code>
            <span>200 : Register.</span>
            <span>400 : Data validation error.</span>
            <span>500 : Internal server error.</span>
        </code>
    </pre>
    """

    serializer_class = RegisterSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def user_data(self, user):
        return UserDetailSerializer(user).data

    def update_user(self, user, password):
        user.set_password(password)
        user.is_actives = True
        user.save()
        return user

    def post(self, request, *args, **kwargs):

        try:

            data = request.data
            data['password']="User@123"
            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
            role = Role.objects.get(id=1)
            user = serializer.save(user_role=role)
            self.update_user(user, serializer.data.get('password'))

            return Response(self.user_data(user), status=http_status.HTTP_200_OK)

        except Exception as e:

            return Response(e.args, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UpdateUserAPIView(APIView):
    """
    API to update user information.
    """

    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:

            get_user = User.objects.get(id=kwargs.get('pk'))
            data1 = UpdateUserSerializer(get_user).data
            return Response({"data1":data1,"message": "Success"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": {"message": str(e)}, "status": status.HTTP_204_NO_CONTENT})

    def put(self,request,*args,**kwargs):
        if id:
            try:
                update_user = User.objects.get(id=kwargs.get("pk"))
            except update_user.DoesNotExist:
                return Response({"msg":"record does not exist"})
            serializer = UpdateUserSerializer(update_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"message":"Success","status":True})
            return Response(serializer.errors)
        return Response({"msg":"please send id"})
    
class CustomPasswordChangeView(PasswordChangeView):

    """
    <h1 id="api_title">Change Password API</h1>
    <p id="api_details">API to change users password takes input as old and new passwords.</p>
    <pre>
        <code>
            API Method : POST
            Token Type : Auth Token ==> Authorization : Token {user-auth-token}
        </code>
    </pre>
    <p id="api_response_title"><strong>Parameters</strong></p>
    <pre>
        <code>
           {
               "old_password": "CharField",  # Old Password (required)
               "new_password1": "CharField",  # New Password 1 (required)
               "new_password2": "CharField",  # New Password 2 (required)
           }
       </code>
   </pre>
    <p id="api_response_title"><strong>Response</strong></p>
    <pre>
        <code>
            {
                "detail": "CharField"
            }
        </code>
    </pre>
    <p id="api_response_title"><strong>API Status</strong></p>
    <pre>
        <code>
            <span>200 : Password Changed.</span>
            <span>400 : Data validation error.</span>
            <span>500 : Internal server error.</span>
        </code>
    </pre>
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    serializer_class = CustomPasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)  # initialize serializer
            serializer.is_valid(raise_exception=True)  # validate serializer
            serializer.save()  # save the data
            return Response({"detail": "New password has been saved."})  # basic success response

        except Exception as e:
            return Response(e.args, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomPasswordResetView(PasswordResetView):

    """
    <h1 id="api_title">Forgot Password API</h1>
    <p id="api_details">API to request for the forgot password. API accept the email address and sends the email.</p>
    <pre>
        <code>
            API Method : POST
            Token Type : Guest Token ==> GUEST-AUTH-TOKEN : {token_provided_by_developer}
        </code>
    </pre>
    <p id="api_response_title"><strong>Parameters</strong></p>
    <pre>
        <code>
           {
               "email": "EmailField",  # Users Email
           }
       </code>
   </pre>
    <p id="api_response_title"><strong>Response</strong></p>
    <pre>
        <code>
            {
                "detail": "CharField"
            }
        </code>
    </pre>
    <p id="api_response_title"><strong>API Status</strong></p>
    <pre>
        <code>
            <span>200 : Forgot password email sent.</span>
            <span>400 : Data validation error.</span>
            <span>500 : Internal server error.</span>
        </code>
    </pre>
    """

    authentication_classes = ()
    permission_classes = (IsTrustedGuest,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = CustomPasswordResetSerializer

    def post(self, request, *args, **kwargs):

        try:
            user = User.objects.filter(email=request.data.get('email'))  # fetch user
            if not user:
                return Response({'message': 'User not found.', 'error': None}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

            serializer.is_valid(raise_exception=True)  # validate the serializer
            serializer.save()  # save the serializer/
            return Response({"message": "Password reset e-mail has been sent.", "error": None},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error_message': str(e.args)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    """
    <h1 id="api_title">Forgot Password Confirm API</h1>
    <p id="api_details">API to set new password. </p>
    <pre>
        <code>
            API Method : POST
            Token Type : Guest Token ==> GUEST-AUTH-TOKEN : {token_provided_by_developer}
        </code>
    </pre>
    <p id="api_response_title"><strong>Parameters</strong></p>
    <pre>
        <code>
           {
                "uid": "CharField",  # Forgot password request uid
                "token": "CharField",  # Forgot password request token
                "new_password1": "CharField",  # New Password 1 (required)
                "new_password2": "CharField",  # New Password 2 (required)
           }
       </code>
   </pre>
    <p id="api_response_title"><strong>Response</strong></p>
    <pre>
        <code>
            {
                "detail": "CharField"
            }
        </code>
    </pre>
    <p id="api_response_title"><strong>API Status</strong></p>
    <pre>
        <code>
            <span>200 : Password set success.</span>
            <span>400 : Data validation error.</span>
            <span>500 : Internal server error.</span>
        </code>
    </pre>
    """

    authentication_classes = ()
    permission_classes = (IsTrustedGuest,)

    serializer_class = CustomPasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Password has been reset with the new password.", "error": None, },
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({ 'error_message': str(e.args)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

###################################################################################################

import cv2
import numpy as np
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
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



def load_known_faces(directory):
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist")

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
                    response = {'data': results[0]}  # Return the first result
                else:
                    response = {'data': 'Not match'}

                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
