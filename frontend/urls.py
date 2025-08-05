from django.urls import path
from .views import index

urlpatterns = [
    path('', index),  # Main endpoint for the frontend
    path('join', index),  # Join endpoint for a specific party
    path('create', index),  # Create endpoint for the frontend
    path('room/<str:roomCode>', index),  # Room endpoint for a specific room
]