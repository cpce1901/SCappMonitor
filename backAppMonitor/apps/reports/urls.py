from django.urls import path
from .views import Report, ReportSensors, ReportFormDetail, ReportFinal, ExportExcel

app_name = 'reports_app'

urlpatterns = [
    path('reportes/', Report.as_view(), name='reports'),
    path("reportes/<int:pk_place>/", ReportSensors.as_view(), name="reportsSensors"),
    path("reportes/<int:pk_place>/<int:pk_sensor>/", ReportFormDetail.as_view(), name="reportForm"),
    path('reportes/<int:pk_place>/<int:pk_sensor>/<str:group>/<str:date1>/<str:date2>/', ReportFinal.as_view(), name='reportFinal'),
    path('reportes/export/<int:pk_place>/<int:pk_sensor>/<str:group>/<str:date1>/<str:date2>/', ExportExcel.as_view(), name='exportExel'),

  
]