from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from apps.sensors.models import Located, Sensor
from apps.lectures.models import Measures
from .form import GrupoForm
from .tasks import export_excel_task
import datetime
import json
import os
from apps.lectures.models import Measures
from apps.sensors.models import Sensor


# Create your views here.
class Report(LoginRequiredMixin, TemplateView):
    template_name = "reports/locatedReport.html"
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


class ReportSensors(LoginRequiredMixin, TemplateView):
    template_name = "reports/sensorReport.html"
    login_url = reverse_lazy("users_app:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place_id = self.kwargs["pk_place"]
        context["sensors"] = Sensor.objects.filter(located_sensor__id=place_id)
        context["place"] = Located.objects.get(id=place_id)
        return context


class ReportFormDetail(LoginRequiredMixin, FormView):
    template_name = "reports/formReport.html"
    form_class = GrupoForm
    login_url = reverse_lazy("users_app:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place_id = self.kwargs["pk_place"]
        sensor_id = self.kwargs["pk_sensor"]
        place = Located.objects.get(id=place_id)
        context["sensor"] = Sensor.objects.get(id=sensor_id)
        context["place"] = place

        return context

    def form_valid(self, form):
        if self.request.method == "POST":
            # Recuperamos las variables desde la URL
            lugar = int(self.kwargs["pk_place"])
            sensor = int(self.kwargs["pk_sensor"])
            grupo = int(form.cleaned_data["grupo"])

            # recuperamos los valores de las fechas limites de inicio y fin y adaptamos para tener una salida standar
            date1 = form.cleaned_data["date1"]
            date2 = form.cleaned_data["date2"]

            date1 = date1.date()
            date2 = date2.date() + datetime.timedelta(days=1)

            date1 = date1.strftime("%Y-%m-%d")
            date2 = date2.strftime("%Y-%m-%d")

            # Validamos los datos para convertir a string y enviarlos a la siguinte vista
            if grupo == 1:
                grupo_envio = "volts-mono"
            elif grupo == 2:
                grupo_envio = "volts-linea"
            elif grupo == 3:
                grupo_envio = "amps"
            elif grupo == 4:
                grupo_envio = "watts"
            elif grupo == 5:
                grupo_envio = "others"
            else:
                grupo_envio = "error"

            # Construimos la url donde visualizaremos todos los datos

            url = reverse_lazy(
                "reports_app:reportFinal",
                kwargs={
                    "pk_place": lugar,
                    "pk_sensor": sensor,
                    "group": grupo_envio,
                    "date1": date1,
                    "date2": date2,
                },
            )

            return redirect(url)

        return super().form_valid(form)


class ReportFinal(LoginRequiredMixin, TemplateView):
    template_name = "reports/reportFinal.html"
    login_url = reverse_lazy("users_app:login")

    # Genera analitica max - min - advantage
    def analitic_values(self, query, var_name):
        name = ""

        if "v" in var_name.lower():
            name = "V"
        elif "i" in var_name.lower():
            name = "A"
        elif "p" in var_name.lower() or var_name.lower() == "pa":
            name = "Kw"

        max_value = max(query)
        min_value = min(query)
        avantage_value = sum([i[0] for i in query]) / len(query)
        vantage_range_date = (query[0][1], query[len(query) - 1][1])

        data = {
            "max": max_value,
            "min": min_value,
            "avantage": avantage_value,
            "dates_avantage": vantage_range_date,
            "var_name": name,
            "var": var_name,
        }

        return data

    # Genera json de grafico
    def create_json(self, query, name):
        list_label = []
        list_data = []

        for a, e in query:
            list_data.append(a)
            fecha = e.strftime("%Y-%m-%d %H:%M:%S")
            list_label.append(fecha)

        data = {
            "data": list_data,
            "labels": list_label,
            "name": name,
        }

        json_response = json.dumps(data)

        return json_response

    # Conseguir detalles de cada consulta v1 - v2 - i1 - pa -etc
    def detail_lecture(self, group):
        """

        "volts-mono"
        "volts-linea"
        "amps"
        "watts"
        "others"
        "error"

        """

        # Define un mapeo de grupos a nombres de columna en la base de datos
        group_to_columns = {
            "volts-mono": ("v1", "v2", "v3"),
            "volts-linea": ("v12", "v23", "v13"),
            "amps": ("i1", "i2", "i3"),
            "watts": ("p1", "p2", "p3"),
            "others": ("pa", "fp", "hz"),
        }

        # Obtiene las columnas correspondientes al grupo
        columns = group_to_columns.get(group, ("", "", ""))

        return columns[0], columns[1], columns[2]

    def get_context_data(self, **kwargs):
        context = super(ReportFinal, self).get_context_data(**kwargs)

        exportExel = {}

        # Recuperamos las variables desde la URL
        place_id = self.kwargs["pk_place"]
        sensor_id = self.kwargs["pk_sensor"]
        vars_group = self.kwargs["group"]
        date1 = self.kwargs["date1"]
        date2 = self.kwargs["date2"]

        # Agregar los elementos al diccionario
        exportExel["pk_place"] = place_id
        exportExel["pk_sensor"] = sensor_id
        exportExel["group"] = vars_group
        exportExel["date1"] = date1
        exportExel["date2"] = date2

        # Conseguimo variables para informe
        user = self.request.user
        today = datetime.date.today()

        # Transformamos datos de fechas en un datetime object
        date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")

        # Restamos 1 dia al dia inicial para obtener datos correctamente
        date1 = date1 - datetime.timedelta(days=1)
        date1 = date1.strftime("%Y-%m-%d+00:00:00")

        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        date2 = date2.strftime("%Y-%m-%d+00:00:00")

        # Conseguimos los detalles desde la consulta que nos interesa
        detail_1, detail_2, detail_3 = self.detail_lecture(vars_group)

        # Realizamos la consulta a db
        datos1 = Measures.objects.list_lectures_sensor_group_detail_dates(
            sensor_id, detail_1, date1, date2
        )
        datos2 = Measures.objects.list_lectures_sensor_group_detail_dates(
            sensor_id, detail_2, date1, date2
        )
        datos3 = Measures.objects.list_lectures_sensor_group_detail_dates(
            sensor_id, detail_3, date1, date2
        )

        try:
            # Creamos los datos json con los datos recibidos desde db
            json1 = self.create_json(datos1, detail_1)
            json2 = self.create_json(datos2, detail_2)
            json3 = self.create_json(datos3, detail_3)

            analitic_1 = self.analitic_values(datos1, detail_1)
            analitic_2 = self.analitic_values(datos2, detail_2)
            analitic_3 = self.analitic_values(datos3, detail_3)

            # Envio de analitica
            context["json_analitics_1"] = analitic_1
            context["json_analitics_2"] = analitic_2
            context["json_analitics_3"] = analitic_3
            # Variable para mostrar data
            show = True

        except:
            show = False

        # Transformamos datos de fechas en un datetime object
        date1 = datetime.datetime.strptime(date1, "%Y-%m-%d+00:00:00")
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d+00:00:00")

        # Envio de datos hacia el template con los datos de grafico
        context["show"] = show

        # Envio de datos hacia el template con los datos de grafico
        context["json_datos_1"] = json1
        context["json_datos_2"] = json2
        context["json_datos_3"] = json3

        context["sensor"] = Sensor.objects.get(id=sensor_id)
        context["today"] = today
        context["date1"] = date1
        context["date2"] = date2
        context["user"] = user
        context["exportExel"] = exportExel

        return context


class ExportExcel(View):
    def get(self, request, *args, **kwargs):
        # Recuperamos las variables desde la URL
        place_id = self.kwargs["pk_place"]
        sensor_id = self.kwargs["pk_sensor"]
        vars_group = self.kwargs["group"]
        date1 = self.kwargs["date1"]
        date2 = self.kwargs["date2"]

        """
        <int:pk_place>/<int:pk_sensor>/<str:group>/<str:date1>/<str:date2>/

        """
        
        # Dispara la tarea Celery para generar el archivo Excel
        result = export_excel_task.delay(
            sensor=sensor_id, vars=vars_group, date1=date1, date2=date2
        )

        # Espera a que la tarea Celery termine y obtiene la ruta del archivo Excel generado
        excel_path = result.get()

        # Abre y lee el archivo Excel
        with open(excel_path, "rb") as excel_file:
            response = HttpResponse(
                excel_file.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        # Configura las cabeceras para la descarga del archivo
        response["Content-Disposition"] = f"attachment; filename=datos.xlsx"

        # Elimina el archivo temporal
        os.remove(excel_path)

        return response
