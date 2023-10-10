from django.urls import path
from .viewset import CreateLectures

app_name = 'lectures_app'

urlpatterns = [
    path('lectures/add/', CreateLectures.as_view(), name='addLecture'),
  
]