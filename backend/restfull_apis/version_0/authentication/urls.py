from django.urls import path, include
from .api import (
    ProtoTypeLookUp,RecognizeFaceAPIView,ComplaintGenericAPI
)


app_name = "authentication"

urlpatterns = [
    path('init/', ProtoTypeLookUp.as_view(), name='init-rest'),

    path('recognize/', RecognizeFaceAPIView.as_view(), name='recognize_face'),

    path('complaint/', ComplaintGenericAPI.as_view(), name='complaint'),
    path('get-complaint/<int:pk>/', ComplaintGenericAPI.as_view(), name='get-complaint'),


]



