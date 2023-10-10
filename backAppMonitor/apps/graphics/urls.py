from django.urls import path
from .views import DayGraphics

app_name = 'graphics_app'

urlpatterns = [
    path("lugares/<int:pk_place>/<int:pk_sensor>/<str:var_name>/", DayGraphics.as_view(), name="daygraphics"),
    
]