from django.db.models import manager, Sum, F, Max, Min, ExpressionWrapper, fields
from django.db.models.functions import TruncMinute, TruncHour, TruncDay, TruncMonth
import datetime


class MeasuresManager(manager.Manager):
    def todo(self):
        return self.all()

    def lecture_last(self, sensor):
        response = self.filter(sensor_id=sensor).last()

        return response

    def list_lectures_sensor_group_dates(self, sensor, group, date1, date2):
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

        response = (
            self.filter(
                sensor_id=sensor,
                # __GTE nos sirve para encontrar el limite inferior incluyendo ese mismo limite
                created__gte=date1,
                # __LTE nos sirve para encontrar el limite superior incluyendo ese mismo limite
                created__lt=date2,
            )
            .prefetch_related("sensor_id")
            .values_list("id", *columns, "created")
            .order_by("created")
        )

        return response

    def list_lectures_sensor_group_detail_dates(self, sensor, detail, date1, date2):
        response = (
            self.filter(
                sensor_id=sensor,
                # __GTE nos sirve para encontrar el limite inferior incluyendo ese mismo limite
                created__gte=date1,
                # __LTE nos sirve para encontrar el limite superior incluyendo ese mismo limite
                created__lt=date2,
            )
            .prefetch_related("sensor_id")
            .values_list(detail, "created")
            .order_by("created")
        )

        return response

    def lectures_today(self, sensor, group):

        # created__gte=2023-10-30+00%3A00%3A00&created__lt=2023-10-31+00%3A00%3A00
        today = datetime.datetime.now()
        date1 = today.strftime("%Y-%m-%d+00:00:00")

        date2 = today + datetime.timedelta(days=1)
        date2 = date2.strftime("%Y-%m-%d+00:00:00")

        response = (
            self.filter(
                sensor_id=sensor,
                # __GTE nos sirve para encontrar el limite inferior incluyendo ese mismo limite
                created__gte=date1,
                # __LTE nos sirve para encontrar el limite superior incluyendo ese mismo limite
                created__lt=date2,
            )
            .values_list(group, "created")
            .order_by("created")
        )

        return response
    

    def lectures_energy_today_by_interval_in_hours(self, sensor):
        today = datetime.datetime.now()
        date1 = today.replace(hour=0, minute=0, second=0, microsecond=0)
        date2 = date1 + datetime.timedelta(days=1)

        queryset = (
        self
        .filter(sensor_id=sensor, created__gte=date1, created__lt=date2)
        .annotate(interval=TruncHour('created'))
        .values('interval')
        .annotate(min_pa=Min('pa'))
        .order_by('interval')
    )

        results = list(queryset)
        for i in range(1, len(results)):
            results[i]['pa_difference'] = results[i]['min_pa'] - results[i-1]['min_pa']

         # Ajuste para el primer registro
        if results:
            results[0]['pa_difference'] = 0

        return results
    

    def lectures_energy_date_range_by_interval(self, sensor, date1, date2, interval):

        
        if interval == 'hour':
            interval_expression = TruncHour('created')
        elif interval == 'day':
            interval_expression = TruncDay('created')
        elif interval == 'month':
            interval_expression = TruncMonth('created')
        else:
            raise ValueError("No existe intervalo valido...")
        
        queryset = (
        self
        .filter(sensor_id=sensor, created__gte=date1, created__lt=date2)
        .annotate(interval=interval_expression)
        .values('interval')
        .annotate(min_pa=Min('pa'))
        .order_by('interval')
        )

        results = list(queryset)
        for i in range(1, len(results)):
            results[i]['pa_difference'] = results[i]['min_pa'] - results[i-1]['min_pa']

         # Ajuste para el primer registro
        if results:
            results[0]['pa_difference'] = 0

        return results

