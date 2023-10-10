from django.shortcuts import get_object_or_404
from django.views.generic import (
    TemplateView,
    UpdateView,
    DeleteView,
    FormView,
    CreateView,
    ListView,
)
from django.urls import reverse_lazy
from .models import Alerts, EmailNotifications
from apps.sensors.models import Sensor
from apps.sensors.models import Sensor, Located
from .form import AlertsAddForm
from collections import defaultdict
from django.contrib import messages


# Create your views here.
class AlertInit(TemplateView):
    template_name = "alerts/alerts.html"


class AlertsSelect(TemplateView):
    template_name = "alerts/alertSelect.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["places"] = Located.objects.all()
        return context


# CRUD Emails


class AlertsGestion(TemplateView):
    template_name = "alerts/alertsSensor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sensor_name = self.kwargs["pk"]
        sensor = Sensor.objects.get(number_sensor=sensor_name)
        alerts = sensor.alerts.all()

        alertas_por_tipo = defaultdict(list)

        for alert in alerts:
            id = alert.id
            alert_type = alert.get_type_name_display()
            value = alert.limit
            level = alert.level
            status = alert.status

            alert_data = {"id": id, "level": level, "value": value, "status": status}

            alertas_por_tipo[alert_type].append((alert_data))

        alert_by_type = dict(alertas_por_tipo)

        context = {"sensor": sensor, "alerts": alert_by_type}

        return context


class AlertCreateForms(FormView):
    template_name = "alerts/alertAdd.html"
    form_class = AlertsAddForm

    # Datos que se envian a template directamente
    def get_context_data(self, **kwargs):
        sensor_name = self.kwargs["sen"]
        context = super().get_context_data(**kwargs)
        context["sensor"] = sensor_name
        return context

    # Procesamiento de formulario valido
    def form_valid(self, form):
        # Nombre para variables de mensaje
        alert_type_name = ""
        level_choices = ""

        # Definimos estructura de datos
        alert_type_choices = {
            "1": "Tension Monofasica",
            "2": "Tension trifasica",
            "3": "Corriente de fase",
            "4": "Potencia de fase",
            "5": "Potencia activa",
            "6": "Factor de potencia",
            "7": "Frecuencia",
        }

        level_choices = {"0": "Low", "1": "High"}

        # Obtenemos datos desde formulario
        type_name = form.cleaned_data["type_name"]
        level = form.cleaned_data["level"]
        limit = form.cleaned_data["limit"]
        status = form.cleaned_data["status"]

        sensor_name = self.kwargs["sen"]
        sensor_instance = Sensor.objects.get(number_sensor=sensor_name)

        # Consultamos si ya existe la alerta procesada
        existing_alert = Alerts.objects.filter(
            sensor=sensor_instance,
            type_name=type_name,
            level=level,
        ).first()

        # Buscamos si es que el sensor ya cuenta con alguna alerta
        if existing_alert:
            # Obtenemos los datos para mostrar en el mensaje de error
            alert_type_name = alert_type_choices.get(type_name, "Desconocido")
            level_name = level_choices.get(level, "Desconocido")

            # mensaje de error en pantalla
            messages.error(
                self.request,
                f"Ya existe una alerta de {alert_type_name} con nivel {level_name}.",
            )

            return self.form_invalid(form)

        alert_instance = Alerts.objects.create(
            type_name=type_name, level=level, limit=limit, status=status
        )

        sensor_instance.alerts.add(alert_instance)

        # Obtenemos los datos para mostrar en el mensaje de error
        alert_type_name = alert_type_choices.get(type_name, "Desconocido")
        level_name = level_choices.get(level, "Desconocido")

        # mensaje de error en pantalla
        messages.success(
            self.request,
            f"La alerta tipo {alert_type_name} de nivel {level_name} ha sido creada con exito.",
        )

        return super().form_valid(form)

    # Redireccion si todo esta bien
    def get_success_url(self):
        sensor_name = self.kwargs["sen"]
        return reverse_lazy(
            "alerts_app:gestionAlertsSensor", kwargs={"pk": sensor_name}
        )


class AlertsUpdateForms(UpdateView):
    template_name = "alerts/alertUpdate.html"
    model = Alerts
    fields = ["type_name", "level", "limit", "status"]

    def get_context_data(self, **kwargs):
        sensor_name = self.kwargs["sen"]
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        context["sensor"] = sensor_name
        context["pk"] = pk
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        alert_instance = get_object_or_404(Alerts, pk=self.kwargs["pk"])
        kwargs["initial"] = {
            "level": alert_instance.level,
            "limit": alert_instance.limit,
            "status": alert_instance.status,
        }
        return kwargs

    def form_valid(self, form):
        print("formulario")
        type_name = form.cleaned_data["type_name"]
        level = form.cleaned_data["level"]

        sensor_name = self.kwargs["sen"]
        sensor_instance = Sensor.objects.get(number_sensor=sensor_name)

        existing_alerts = Alerts.objects.filter(
            sensor=sensor_instance,
            type_name=type_name,
            level=level,
        ).exclude(pk=self.object.pk)

        if existing_alerts.exists():
            alert_type_choices = {
                "1": "Tension Monofasica",
                "2": "Tension trifasica",
                "3": "Corriente de fase",
                "4": "Potencia de fase",
                "5": "Potencia activa",
                "6": "Factor de potencia",
                "7": "Frecuencia",
            }

            level_choices = {"0": "Low", "1": "High"}

            alert_type_name = alert_type_choices.get(type_name, "Desconocido")
            level_name = level_choices.get(level, "Desconocido")

            form.add_error(
                None,
                f"Ya existe una alerta de {alert_type_name} con nivel {level_name}.",
            )
            return self.form_invalid(form)

        self.object = form.save(commit=False)
        self.object.sensor = sensor_instance
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        sensor_name = self.kwargs["sen"]
        return reverse_lazy(
            "alerts_app:gestionAlertsSensor", kwargs={"pk": sensor_name}
        )


class AlertDeleteForm(DeleteView):
    template_name = "alerts/alertDelete.html"
    model = Alerts

    def get_context_data(self, **kwargs):
        sensor_name = self.kwargs["sen"]
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        context["sensor"] = sensor_name
        context["pk"] = pk
        return context

    def get_success_url(self):
        sensor_name = self.kwargs["sen"]
        return reverse_lazy(
            "alerts_app:gestionAlertsSensor", kwargs={"pk": sensor_name}
        )


# CRUD Emails


class EmailList(ListView):
    template_name = "alerts/emailsList.html"
    model = EmailNotifications
    context_object_name = "emails"


class EmailAdd(CreateView):
    template_name = "alerts/emailAdd.html"
    model = EmailNotifications
    fields = "__all__"
    success_url = reverse_lazy("alerts_app:emailList")


class EmailDelete(DeleteView):
    template_name = "alerts/emailDelete.html"
    model = EmailNotifications
    success_url = reverse_lazy("alerts_app:emailList")


class EmailUpdate(UpdateView):
    template_name = "alerts/emailUpdate.html"
    model = EmailNotifications
    fields = "__all__"
    success_url = reverse_lazy("alerts_app:emailList")
