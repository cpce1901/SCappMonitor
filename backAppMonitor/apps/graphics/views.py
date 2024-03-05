from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.lectures.models import Measures
from apps.sensors.models import Sensor, Located
import json
import datetime


# Create your views here.
class DayGraphics(LoginRequiredMixin, TemplateView):
    template_name = "graphics/daygraphics.html"
    login_url = reverse_lazy("users_app:login")

    # Genera json de grafico
    def create_json(self, query, name):
        name_var = ""
        if name in ["v1", "v2", "v3"]:
            unit = "V"
            name_var = "Tensión de fase"
        elif name in ["v13", "v12", "v23"]:
            unit = "V"
            name_var = "Tensión de línea"
        elif name in ["i1", "i2", "i3"]:
            unit = "A"
            name_var = "Corriente de fase"
        elif name in ["p1", "p2", "p3"]:
            unit = "Kw"
            name_var = "Potencia de fase"
        elif name == "ea":
            unit = "Kw/h"
            name_var = "Energía activa"
        elif name == "fp":
            unit = ""
            name_var = "Factor de potencia"
        elif name == "hz":
            unit = "Hz"
            name_var = "Frecuencia"
        elif name == "pa":
            unit = "kw/h"
            name_var = "Energía"

        list_label = []
        list_data = []

        if name == "ea":
            for data in query:
                e = data['interval']
                list_data.append(str(round(data['pa_difference'],2)))
                fecha = e.strftime("%Y-%m-%d %H:%M:%S")
                list_label.append(fecha)
                
        else:
            for a, e in query:
                list_data.append(str(round(a,2)))
                fecha = e.strftime("%Y-%m-%d %H:%M:%S")
                list_label.append(fecha)

     
        if len(list_data) and len(list_label):
            show = True
        else:
            show = False

        data = {
            "data": list_data,
            "labels": list_label,
            "name": name_var,
            "unit": unit,
        }

        json_response = json.dumps(data)

        return show, json_response

    def get_context_data(self, **kwargs):
        date = datetime.date.today()

        context = super().get_context_data(**kwargs)
        place_id = self.kwargs["pk_place"]
        sensor_id = self.kwargs["pk_sensor"]
        var_name = self.kwargs["var_name"]

        var = ""
        text = ""

        variable_mapping = {
            "v1": ("Voltaje monofásico", "Línea 1"),
            "v2": ("Voltaje monofásico", "Línea 2"),
            "v3": ("Voltaje monofásico", "Línea 3"),
            "v12": ("Voltaje trifásico", "Línea 1 - Línea 2"),
            "v13": ("Voltaje trifásico", "Línea 1 - Línea 3"),
            "v23": ("Voltaje trifásico", "Línea 2 - Línea 3"),
            "i1": ("Corriente de línea", "Línea 1"),
            "i2": ("Corriente de línea", "Línea 2"),
            "i3": ("Corriente de línea", "Línea 3"),
            "p1": ("Potencia de línea", "Línea 1"),
            "p2": ("Potencia de línea", "Línea 2"),
            "p3": ("Potencia de línea", "Línea 3"),
            "pa": ("Energía", ""),
            "fp": ("Factor de potencia", ""),
            "hz": ("Frecuencia", ""),
        }

        if var_name in variable_mapping:
            var, text = variable_mapping[var_name]

        sensor = Sensor.objects.get(id=sensor_id)
        place = Located.objects.get(id=place_id)
    
        datos = Measures.objects.lectures_today(sensor.number_sensor, var_name)

        # Creamos los datos json con los datos recibidos desde db
        show, json_data = self.create_json(datos, var_name)

        context["show"] = show
        context["sensor"] = sensor
        context["place"] = place
        context["today"] = json_data
        context["var"] = (var, text)
        context["date"] = date
        return context


