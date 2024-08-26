from django.utils.translation import gettext as _
from rest_framework import serializers
from users.models import Complaint



class FaceRecognitionSerializer(serializers.Serializer):
    image = serializers.ImageField()
    # known_faces_dir = serializers.CharField()

class ComplaintSerialzier(serializers.Serializer):

    class Meta:
        fields = "__all__"
