from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainp, name='mainp'),
    path('serach/', views.serach, name='serach'),
]