from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.lectures.models import Measures
from apps.sensors.models import Sensor, Located
import json

# Create your views here.
class DayGraphics(LoginRequiredMixin, TemplateView):
    template_name = "graphics/daygraphics.html"
    login_url = reverse_lazy("users_app:login")

    # Genera json de grafico
    def create_json(self, query, name):
        list_label = []
        list_data = []

        for a, e in query:
            list_data.append(a)
            fecha = e.strftime("%Y-%m-%d %H:%M:%S")
            list_label.append(fecha)

        data = {
            "data": list_data,
            "labels": list_label,
            "name": name,
        }

        json_response = json.dumps(data)

        return json_response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place_id = self.kwargs["pk_place"]
        sensor_id = self.kwargs["pk_sensor"]
        var_name = self.kwargs["var_name"]

        sensor = Sensor.objects.get(id=sensor_id)

        datos = Measures.objects.lectures_today(sensor.number_sensor, var_name)

        # Creamos los datos json con los datos recibidos desde db
        json_data = self.create_json(datos, var_name)

        place = Located.objects.get(id=place_id)
        context["sensor"] = sensor.number_sensor
        context["place"] = place
        context["today"] = json_data
        return context
