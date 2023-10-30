from celery import shared_task
from openpyxl import Workbook
from apps.lectures.models import Measures
import os


def detail_lecture(group):
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


@shared_task(name="reporte")
def export_excel_task(sensor, vars, date1, date2):
    try:
        detail_1, detail_2, detail_3 = detail_lecture(vars)

        datos = Measures.objects.list_lectures_sensor_group_dates(
            sensor, vars, date1, date2
        )

        # Crea un nuevo libro de trabajo Excel
        wb = Workbook()
        ws = wb.active

        # Agrega encabezados de columna
        ws.append(
            ["ID", detail_1, detail_2, detail_3, "Fecha"]
        )  # Reemplaza con tus nombres de columna

        # Agrega datos a las filas
        for dato in datos:
            ws.append(
                [dato[0], dato[1], dato[2], dato[3], dato[4]]
            )  # Reemplaza con los nombres de tus campos

        # Guarda el archivo Excel
        excel_filename = "datos.xlsx"
        excel_path = os.path.join(
            "media", excel_filename
        )  # Asegúrate de que 'media' sea una carpeta válida en tu proyecto
        wb.save(excel_path)

        print("este es el path", excel_path)
        return excel_path

    except Exception as e:
        # Manejo de excepciones
        # Registra el error o realiza acciones de recuperación según sea necesario
        print(f"Error en export_excel_task: {str(e)}")
        return None
