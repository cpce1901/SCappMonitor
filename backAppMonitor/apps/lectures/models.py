from django.db import models
from apps.sensors.models import Sensor
from .manager import MeasuresManager

# Create your models here.
class Measures(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, verbose_name='Sensor N°', db_index=True)
    v1 = models.FloatField('V L1 - N', db_index=True)
    v2 = models.FloatField('V L2 - N', db_index=True)
    v3 = models.FloatField('V L3 - N', db_index=True)

    v13 = models.FloatField('V L1 - L3', db_index=True)
    v12 = models.FloatField('V L1 - L2', db_index=True)
    v23 = models.FloatField('V L2 - L3', db_index=True)

    i1 = models.FloatField('I L1', db_index=True)
    i2 = models.FloatField('I L2', db_index=True)
    i3 = models.FloatField('I L3', db_index=True)

    p1 = models.FloatField('P L1', db_index=True)
    p2 = models.FloatField('P L2', db_index=True)
    p3 = models.FloatField('P L3', db_index=True)

    pa = models.FloatField('PA', db_index=True)
    fp = models.FloatField('FP', db_index=True)
    hz = models.FloatField('Hz', db_index=True)

    #created = models.DateTimeField('Fecha de creación', auto_now_add=True, db_index=True)
    created = models.DateTimeField('Fecha de creación', db_index=True)

    objects = MeasuresManager()

    class Meta:
        verbose_name = 'Medida'
        verbose_name_plural = 'Medidas'
        

    def __str__(self):
        return f'{self.sensor}'