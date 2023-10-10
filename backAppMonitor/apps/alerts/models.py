from django.core.exceptions import ValidationError
from django.db import models


class EmailNotifications(models.Model):
    name = models.CharField("Nombre", max_length=256)
    email = models.EmailField("Correo")

    class Meta:
        verbose_name = "Correo notificaciones"
        verbose_name_plural = "Correos notificaciones"

    def __str__(self):
        return f"{self.email} - {self.name}"


class Alerts(models.Model):
    alert_type_choices = [
        ("1", "Tension Monofasica"),
        ("2", "Tension trifasica"),
        ("3", "Corriente de línea"),
        ("4", "Potencia de fase"),
        ("5", "Potencia activa"),
        ("6", "Factor de potencia"),
        ("7", "Frecuencia"),
    ]

    level_choices = [("0", "Low"), ("1", "High")]

    type_name = models.CharField(
        "Tipo de alerta", max_length=1, choices=alert_type_choices
    )

    level = models.CharField("Nivel de alerta", max_length=1, choices=level_choices)
    limit = models.FloatField("Limite")
    status = models.BooleanField("Estado")

    class Meta:
        verbose_name = "Tipo de alerta"
        verbose_name_plural = "Tipos de alertas"

    def type_alert(self):
        for option_value, option_display in self.alert_type_choices:
            if option_value == self.type_name:
                return option_display
        return "Desconocido"

    def level_alert(self):
        for option_value, option_display in self.level_choices:
            if option_value == self.level:
                return option_display
        return "Desconocido"

    type_alert.short_description = "Tipo de alerta"
    level_alert.short_description = "Nivel de alerta"

    def __str__(self):
        return f"{self.type_alert()} - {self.level_alert()} - {self.limit}"
