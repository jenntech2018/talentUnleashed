from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('about/', views.about, name='about'),
    path('partners/', views.partners, name='partners'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
