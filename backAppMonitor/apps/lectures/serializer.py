from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Measures

class LectureSerializer(ModelSerializer):
    class Meta:
        model = Measures
        fields = '__all__'

    