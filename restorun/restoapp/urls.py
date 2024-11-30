from django.urls import path
from . import views


urlpatterns = [
   path('', views.openapp, name = "openapp"),
]