from django.urls import path
from .views import login, signup, emailverification

urlpatterns = [
    path('login', login),
    path('signup', signup),
    path('verify', emailverification)
]
