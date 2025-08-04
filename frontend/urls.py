from django.urls import path
from .views import index

urlpatterns = [
    path('', index),  # Main endpoint for the frontend
    path('join', index),  # Join endpoint for the frontend
    path('create', index),  # Create endpoint for the frontend
    path('join/1', index),  # Join endpoint for a specific party
]