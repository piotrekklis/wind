from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_observations/', views.getObservations, name='get_observations'),
    path('get_localizations/', views.getLocalizations, name='get_localizations'),
    path('test/', views.test, name='test')
]
