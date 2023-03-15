from django.urls import path
from . import views

urlpatterns = [
    path('linrank/', views.linrank, name='linrank'),
]