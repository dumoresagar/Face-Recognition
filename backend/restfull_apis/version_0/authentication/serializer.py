from django.utils.translation import gettext as _
from rest_framework import serializers




class FaceRecognitionSerializer(serializers.Serializer):
    image = serializers.ImageField()
    # known_faces_dir = serializers.CharField()