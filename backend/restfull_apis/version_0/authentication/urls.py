from django.urls import path, include
from .api import (
    ProtoTypeLookUp,RecognizeFaceAPIView
)


app_name = "authentication"

urlpatterns = [
    path('init/', ProtoTypeLookUp.as_view(), name='init-rest'),

    path('recognize/', RecognizeFaceAPIView.as_view(), name='recognize_face'),

]



