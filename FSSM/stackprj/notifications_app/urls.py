# notifications_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_notifications/', views.get_notifications, name='get_notifications'),
]
