# notifications_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import BroadcastNotification

def get_notifications(request):
    notifications = BroadcastNotification.objects.filter(sent=False)
    notifications_data = [{"message": n.message, "broadcast_on": n.broadcast_on} for n in notifications]
    return JsonResponse(notifications_data, safe=False)
