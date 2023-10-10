from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import Tag, Device, Located, Sensor


# Register your models here.
class LocatedAdmin(admin.ModelAdmin):
    list_display = ["place", "sensor_count", "sensors_list"]
    ordering = ["created"]

    def get_queryset(self, request):
        # Anulamos el queryset para agregar la anotación con el recuento de sensores
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(sensor_count=models.Count("located"))

        return queryset

    def sensor_count(self, obj):
        return obj.sensor_count

    def sensors_list(self, obj):
        response = Sensor.objects.filter(located_sensor=obj.id)
        sensors = [f"<li>{sensor.detail}</li>" for sensor in response]

        if sensors:
            sensors_html = "<ul>" + "".join(sensors) + "</ul>"
            return format_html(sensors_html)
        else:
            return "No existen sensores"

    sensor_count.short_description = "Cantidad de Sensores"
    sensors_list.short_description = "Lista de sensores"


class SensorAdmin(admin.ModelAdmin):
    list_display = ("number_sensor", "device_sensor", "located_sensor", "detail", "show_alerts")
    list_filter = [
        "located_sensor",
    ]
    ordering = ("located_sensor",)
    filter_horizontal = ["alerts"]

    def show_alerts(self, obj):
        alerts = obj.alerts.all()
        alerts_list = [f"<li>{alert.get_type_name_display()}</li>" for alert in alerts]

        if alerts_list:
            alerts_html = "<ul>" + "".join(alerts_list) + "</ul>"
            return format_html(alerts_html)
        else:
            return "No existen alertas"

    show_alerts.short_description = "Alertas"


class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]


class DeviceAdmin(admin.ModelAdmin):
    list_display = ["code", ]


admin.site.register(Tag, TagAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Located, LocatedAdmin)
admin.site.register(Sensor, SensorAdmin)
