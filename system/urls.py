# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.page_info, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('productos/', views.productos, name='productos'),
    path('productos/<str:categoria>/', views.productosCategoria, name='productosCategoria'),

    path('configuracion/guardar/', views.guardar_configuracion, name='guardar_configuracion'),
    path('producto/guardar/', views.registrar_producto, name='crearProducto'),
]