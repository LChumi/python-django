from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('visualizacion_datos/', views.visualizacion_datos, name='visualizacion_datos'),
    path('calcular_imc/', views.calcular_imc, name='calcular_imc'),
    path('frecuencia_cardiaca/', views.frecuencia_cardiaca, name='frecuencia_cardiaca'),
    path('simular_datos/', views.simular_datos, name='simular_datos'),
]
