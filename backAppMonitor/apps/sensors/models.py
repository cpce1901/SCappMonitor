from django.db import models
from .manager import SensorManager
from apps.alerts.models import Alerts
from stdimage import StdImageField


# Create your models here.


class Tag(models.Model):
    name = models.CharField("Nombre de marca", max_length=50, unique=True)
    created = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return f"{self.name}"


class Device(models.Model):
    tag_device = models.ForeignKey(
        Tag, on_delete=models.CASCADE, verbose_name="Marca", related_name="tag"
    )
    code = models.CharField("Modelo", max_length=50, unique=True)
    description = models.CharField("Descripción", max_length=255)
    imagen_device = StdImageField(
        "Imagen de equipo",
        unique=True,
        upload_to="media/device",
        variations={"option": {"width": 720, "height": 720, "crop": True}},
    )
    created = models.DateTimeField("Fecha de creación", auto_now_add=True)

    def __str__(self):
        return f"{self.tag_device} - {self.code}"

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"


class Located(models.Model):
    place = models.CharField("Lugar de instalación", max_length=50)
    image = StdImageField(
        "Imagen de lugar",
        unique=True,
        upload_to="media/located",
        blank=True,
        variations={"option": {"width": 720, "height": 720, "crop": True}},
    )
    created = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "Ubicacion"
        verbose_name_plural = "Ubicaciones"

    def __str__(self):
        return f"{self.place}"


class Sensor(models.Model):
    number_sensor = models.SmallIntegerField("Numero sensor", unique=True)
    device_sensor = models.ForeignKey(
        Device, on_delete=models.CASCADE, verbose_name="Equipo", related_name="device"
    )
    located_sensor = models.ForeignKey(
        Located,
        on_delete=models.CASCADE,
        verbose_name="Ubicación",
        related_name="located",
    )

    alerts = models.ManyToManyField(Alerts, blank=True)

    detail = models.CharField("Detalle", max_length=256, blank=True)

    created = models.DateTimeField("Fecha de creación", auto_now_add=True)

    objects = SensorManager()

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensores"

    def __str__(self):
        return f"{self.id}"
