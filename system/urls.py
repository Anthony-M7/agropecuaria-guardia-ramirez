# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.page_info, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
]