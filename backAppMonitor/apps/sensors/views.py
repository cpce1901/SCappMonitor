from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.conf import settings
from .models import Sensor, Located
from apps.lectures.models import Measures
import json


# Create your views here.
class ListPlaces(LoginRequiredMixin, TemplateView):
    template_name = "sensors/located.html"
    login_url = reverse_lazy("users_app:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ubicaciones_con_sensores = Located.objects.annotate(
            num_sensores=Count("located")
        ).order_by("id")
        context["places"] = ubicaciones_con_sensores

        return context

    def get_queryset(self):
        return Located.objects.order_by("id")


class ListSensors(LoginRequiredMixin, TemplateView):
    template_name = "sensors/sensors.html"
    login_url = reverse_lazy("users_app:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place_id = self.kwargs["pk_place"]
        context["sensors"] = Sensor.objects.filter(located_sensor__id=place_id)
        context["place"] = Located.objects.get(id=place_id)
        return context


class DetailMeasures(LoginRequiredMixin, TemplateView):
    template_name = "sensors/measures.html"
    login_url = reverse_lazy("users_app:login")

    def create_data_json(self, locate, sensor):
        broker = settings.BROKER_MQTT
        port = settings.PORT
        base = settings.CLIENTE
        data = (
            {
                "server": broker,
                "port": port,
                "user": settings.USER,
                "pass": settings.PASS,
                "base": base,
                "ubicacion": str(locate).replace(" ", ""),
                "sensor": sensor,
            },
            
        )

        return json.dumps(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place_id = self.kwargs["pk_place"]
        sensor_id = self.kwargs["pk_sensor"]
        place = Located.objects.get(id=place_id)
        context["sensor"] = Sensor.objects.get(id=sensor_id)
        context["place"] = place
        context["lectures"] = Measures.objects.lecture_last(sensor_id)
        context["json_data"] = self.create_data_json(place.place, sensor_id)
        return context
    



