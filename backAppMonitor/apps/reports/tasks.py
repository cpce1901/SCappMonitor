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

        # Crea un nuevo libro de trabajo Excel
        wb = Workbook()
        ws = wb.active

        if 'kwh' in vars or 'hz' in vars or 'fp' in vars:
            detail = 'pa' if 'kwh' in vars else str(vars)
            datos = Measures.objects.list_lectures_sensor_group_detail_dates(sensor, detail, date1, date2)
            print(datos)
            # Agrega encabezados de columna
            ws.append(
                ["ID", detail, "Fecha"]
            )  # Reemplaza con tus nombres de columna

            # Agrega datos a las filas
            for dato in datos:
                ws.append(
                    [dato[0], dato[1], dato[2]]
                ) 
        else:
            detail_1, detail_2, detail_3 = detail_lecture(vars)
            datos = Measures.objects.list_lectures_sensor_group_dates(sensor, vars, date1, date2)

            # Agrega encabezados de columna
            ws.append(
                ["ID", detail_1, detail_2, detail_3, "Fecha"]
            )  # Reemplaza con tus nombres de columna

            # Agrega datos a las filas
            for dato in datos:
                ws.append(
                    [dato[0], dato[1], dato[2], dato[3], dato[4]]
                )
       
        # Guarda el archivo Excel
        excel_filename = "datos.xlsx"
        excel_path = os.path.join(
            "media", excel_filename
        )
        wb.save(excel_path)
        return excel_path

    except Exception as e:
        print(f"Error en export_excel_task: {str(e)}")
        return None
