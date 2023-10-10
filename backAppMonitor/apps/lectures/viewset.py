from rest_framework.generics import CreateAPIView
from .serializer import LectureSerializer

class CreateLectures(CreateAPIView):
    serializer_class = LectureSerializer
    