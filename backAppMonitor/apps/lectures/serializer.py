from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Measures

class LectureSerializer(ModelSerializer):
    class Meta:
        model = Measures
        fields = '__all__'

    
    def validate(self, data):
        for i in data:
            
            if i == "created" or i == "sensor":
                pass
            else:
                if data[i] > 1500:
                    raise ValidationError(f"Valores en {i}: {data[i]} mayores a 1000...") 
                
        return data
        

        
        