from django.urls import path
from .views import DayGraphics, EnergyGraphic

app_name = 'graphics_app'

urlpatterns = [
    path("lugares/<str:var_name>/<int:pk_place>/<int:pk_sensor>/", DayGraphics.as_view(), name="daygraphics"),
    path("lugares/energia/<int:pk_place>/<int:pk_sensor>/<str:interval>/", EnergyGraphic.as_view(), name="energygraphics"),
    
]