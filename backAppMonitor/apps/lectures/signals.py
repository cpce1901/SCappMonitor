from django.db.models.signals import post_save
from .models import Measures
from django.dispatch import receiver
from apps.sensors.models import Sensor
from .tasks import send_email_alert


# La funcion evalua, el nivel alto o bajo, su numero limite,
# el name es el nombre de la variable o variables
# y los argumentos son los valores recividos en el endpoint


def validate(level, limit, names, *args):
    # Variable para rastrear cuál es mayor o menor
    mayor_menor = None

    # Si nivel contiene un valor, aunque siempre deberia tenerlo
    # 0 bajo
    # 1 alto

    if level == "0" or level == "1":
        # Realiza un for para revisar todos los valores en los argumentos pasados
        # i corresponde al nombre de los argumentos entregados
        # value corresponde al valor numerico en esos argumentos
        for i, value in enumerate(args):
            # Realliza revision en caso de un nivel bajo 
            # Realiza revision si el limite esta bajo el limite
            if level == "0" and value < limit:
                # Crea mensaje en caso de ser verdadera esta consicion y sale del ciclo
                mayor_menor = (
                    f"{names[i]} {value} es menor al límite {limit} de alarma seteado"
                )
                break
            elif level == "1" and value > limit:
                mayor_menor = (
                    f"{names[i]} {value} es mayor al límite {limit} de alarma seteado"
                )
                break

    if mayor_menor:
        send_email_alert.delay(mayor_menor)
        print(f"Enviar correo: {mayor_menor}")
    else:
        print("Enviar correo: Valores normalizados")

    return mayor_menor


# Revida datos desde el sensor que ha llegado
@receiver(post_save, sender=Measures)
def review_lecture_for_alert(sender, instance, **kargs):
    sensor_id = instance.sensor.id
    sensor = Sensor.objects.get(number_sensor=sensor_id)
    alerts = sensor.alerts.all()

    """
    ("1", "Tension Monofasica"),
    ("2", "Tension trifasica"),
    ("3", "Corriente de línea"),
    ("4", "Potencia de fase"),
    ("5", "Potencia activa"),
    ("6", "Factor de potencia"),
    ("7", "Frecuencia")

    """
    names = []
    for i in alerts:
        if i.status:
            if i.type_name == "1":
                # evalua en tension monofasica
                names = ["Voltaje L1", "Voltaje L2", "Voltaje L3"]
                validate(i.level, i.limit, names, instance.v1, instance.v2, instance.v3)
            elif i.type_name == "2":
                # evalua en tension trifasica
                names = ["Voltaje L13", "Voltaje L23", "Voltaje L23"]
                validate(
                    i.level, i.limit, names, instance.v13, instance.v23, instance.v23
                )
            elif i.type_name == "3":
                # evalua en corriente de linea
                names = ["Corriente L1", "Corriente L2", "Corriente L3"]
                validate(i.level, i.limit, names, instance.i1, instance.i2, instance.i3)
            elif i.type_name == "4":
                # evalua en potencia de fase
                names = ["Potencia L1", "Potencia L2", "Potencia L3"]
                validate(i.level, i.limit, names, instance.p1, instance.p2, instance.p3)
            elif i.type_name == "5":
                # evalua en potencia activa
                names = ["Potencia activa"]
                validate(i.level, i.limit, names, instance.pa)
            elif i.type_name == "6":
                # evalua en factor de potencia
                names = ["Factor de potencia"]
                validate(i.level, i.limit, names, instance.fp)
            elif i.type_name == "7":
                # evalua en frecuencia
                names = ["Frecuencia"]
                validate(i.level, i.limit, names, instance.hz)
            pass

    return None


