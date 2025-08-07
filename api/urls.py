from django.urls import path

from .views import RoomView, CreateRoomView, GetRoom, JoinRoom

"""
URL configuration for the API endpoints.
This file defines the URL patterns for the API views.
"""

urlpatterns = [
    path('room', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path('get-room', GetRoom.as_view()),
    path('join-room', JoinRoom.as_view()),
]