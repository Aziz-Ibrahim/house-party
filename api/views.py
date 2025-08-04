from django.shortcuts import render
from rest_framework import generics

from .models import Room
from .serializers import RoomSerializer


class RoomView(generics.ListAPIView):
    """
    API view to create a new room.
    Inherits from CreateAPIView to handle POST requests for creating a room.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer