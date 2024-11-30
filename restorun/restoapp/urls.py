from django.urls import path
from . import views


urlpatterns = [
   path('', views.list_items, name='list_items'),
   path('add/', views.add_item, name='add_item'),
   path('delete/<int:pk>/', views.delete_item, name='delete_item'),
   path('search/', views.search_items, name='search_items'),
]