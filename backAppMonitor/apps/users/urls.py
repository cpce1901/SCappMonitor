from django.urls import path
from .views import Login, Logout, UpdatePass, DetailUser

app_name = 'users_app'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('change-pass/', UpdatePass.as_view(), name='change-pass'),
    path('usuarios/', DetailUser.as_view(), name='user'),
]