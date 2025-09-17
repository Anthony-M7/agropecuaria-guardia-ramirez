from django.urls import path
from .views import CustomLoginView, CustomLogoutView, custom_user_add
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rutas de autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Rutas personalizadas para la recuperación de contraseña
    path('password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    path('register/', custom_user_add, name='custom_user_add'),
]

