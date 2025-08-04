from django.urls import path
from .views import main

urlpatterns = [
    path('', main),  # Main endpoint for the API
]