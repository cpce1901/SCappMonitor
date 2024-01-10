from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Measures

class LectureSerializer(ModelSerializer):
    class Meta:
        model = Measures
        fields = '__all__'

    def validate(self, data):
        # Obtén el último objeto Measures para el mismo sensor
        last_measure = Measures.objects.filter(sensor=data['sensor']).order_by('-created').first()

        # Verifica si hay un registro anterior para comparar
        if last_measure:
            # Definir la cantidad máxima permitida de diferencia
            max_allowed_difference = 300  # Ajusta según tus necesidades

            # Validar la diferencia para cada campo
            for field in ['v1', 'v2', 'v3', 'v13', 'v12', 'v23', 'i1', 'i2', 'i3', 'p1', 'p2', 'p3', 'pa', 'fp', 'hz']:
                new_value = data.get(field, 0)
                last_value = getattr(last_measure, field, 0)

                if abs(new_value - last_value) > max_allowed_difference:
                    raise ValidationError({field: f'Diferencia demasiado grande en {field}'})
        
        return data