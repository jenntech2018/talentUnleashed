from django.urls import path
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('thank-you/', views.thank_you, name='thank_you'),
]