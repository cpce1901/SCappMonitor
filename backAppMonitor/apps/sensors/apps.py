from django.apps import AppConfig
from django.core.signals import setting_changed


class SensorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sensors"

    def ready(self):
        from. import signals
