from django.urls import path
from .views import  AlertsSelect, AlertInit, AlertsGestion, AlertsUpdate, AlertDeleteForm, AlertCreateForms, EmailList, EmailAdd, EmailDelete, EmailUpdate

app_name = 'alerts_app'

urlpatterns = [
    path("alertas/", AlertInit.as_view(), name="alerts"),
    path("alertas/gestion/", AlertsSelect.as_view(), name="gestionAlerts"),
    path("alertas/gestion/<int:pk>/", AlertsGestion.as_view(), name="gestionAlertsSensor"),

    path("alertas/gestion/form/<int:sen>/", AlertCreateForms.as_view(), name="alertCreateForm"),
    path("alertas/gestion/form/<int:sen>/<int:pk>/", AlertsUpdate.as_view(), name="alertUpdateForm"),
    path("alertas/gestion/form/borrar/<int:sen>/<int:pk>/", AlertDeleteForm.as_view(), name="alertDeleteForm"),

    path("alertas/emails/", EmailList.as_view(), name="emailList"),
    path("alertas/emails/add/", EmailAdd.as_view(), name="emailAdd"),
    path("alertas/emails/delete/<int:pk>/", EmailDelete.as_view(), name="emailDelete"),
    path("alertas/emails/update/<int:pk>/", EmailUpdate.as_view(), name="emailUpdate"),
]