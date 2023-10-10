from django.contrib import admin
from django.utils.html import format_html
from .models import Alerts, EmailNotifications
from apps.sensors.models import Sensor


class AletAdmin(admin.ModelAdmin):
    list_display = ["type_name", "level", "limit", "status", "sensor_asigned"]
   

    def sensor_asigned(self, obj):
        sensor = Sensor.objects.filter(alerts__level=obj.level, alerts__limit=obj.limit)
        sensors = [
            f"<li>{sensor.located_sensor.place} - Sensor: {sensor.id} - {sensor.detail}</li>" for sensor in sensor
        ]

        if not sensors:
            return "No existen sensores asociados"
        elif sensors and len(sensor) <= 6:
            sensors_html = "<ul>" + "".join(sensors) + "</ul>"
            return format_html(sensors_html)
        else:
            return "Todos"

    sensor_asigned.short_description = "Detalles sensor"


admin.site.register(Alerts, AletAdmin)
admin.site.register(EmailNotifications)
