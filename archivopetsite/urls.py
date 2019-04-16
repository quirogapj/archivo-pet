from django.urls import path
from django.urls import include, path
from django.conf.urls import url



from . import views


urlpatterns = [
    #path('', views.mascota_new, name='mascota_new'),
    url(r'^$', views.index, name='index'),
    path('mascota/lista/', views.mascota_list, name='mascota_list'),
    path('mascota/<int:pk>/', views.mascota_detail, name='mascota_detail'),
    path('mascota/new/', views.mascota_new, name='mascota_new'),
    path('mascota/<int:pk>/edit/', views.mascota_edit, name='mascota_edit'),
    url(r'^buscar_mascota/$', views.search_form),
    url(r'^buscar/$', views.search),
    path('contacto/', views.emailView, name='email'),
    path('success/', views.successView, name='success'),
]
