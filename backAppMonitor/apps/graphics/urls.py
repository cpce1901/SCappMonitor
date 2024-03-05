from django.urls import path
from .views import DayGraphics

app_name = 'graphics_app'

urlpatterns = [
    path("lugares/<str:var_name>/<int:pk_place>/<int:pk_sensor>/", DayGraphics.as_view(), name="daygraphics"),
    
]