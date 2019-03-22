from django.urls import path
from django.urls import include, path

from . import views


urlpatterns = [
    #path('', views.mascota_new, name='mascota_new'),
    path('', views.mascota_list, name='mascota_list'),
    path('mascota/<int:pk>/', views.mascota_detail, name='mascota_detail'),
    path('mascota/new/', views.mascota_new, name='mascota_new'),
    path('mascota/<int:pk>/edit/', views.mascota_edit, name='mascota_edit'),
]
