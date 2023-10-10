from django.db import models
from django.db.models import Subquery, OuterRef, Case, When, Value, CharField
from apps.alerts.models import Alerts


class SensorManager(models.Manager):
    def todo(self):
        return self.all()

    def alert_by_type(self, sensor, type):
        try:
            sensor = self.get(number_sensor=sensor)
            alerts = sensor.alerts.filter(type_name=type)
            return sensor, alerts
        except self.DoesNotExist:
            return None, []


