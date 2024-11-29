
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.formulario_view, name='formulario_view'),
    path('estado/', views.generarreportes_view, name='generarreportes_view'),
    path('generar-reporte-pago/', views.generarReportePago, name='generarReportePago'),
]
