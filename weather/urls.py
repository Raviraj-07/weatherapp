from django.urls import path
from .views import getweather

urlpatterns = [
    path('weather', getweather)
]
