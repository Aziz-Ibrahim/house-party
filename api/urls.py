from django.urls import path

from .views import RoomView, CreateRoomView

"""
URL configuration for the API endpoints.
This file defines the URL patterns for the API views.
"""

urlpatterns = [
    path('room', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view())
]