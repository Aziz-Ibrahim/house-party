from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer


class RoomView(generics.ListAPIView):
    """
    API view to create a new room.
    Inherits from CreateAPIView to handle POST requests for creating a room.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    """
    API view to handle room creation.
    Inherits from APIView to define custom behavior for POST requests.
    """
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        """
        Handle POST request to create a new room.
        Validates the request data and creates a new Room instance.
        """
        if not self.request.session.exists(request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guests_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guests_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_200_OK
                )
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guests_can_pause,
                    votes_to_skip=votes_to_skip
                )
                room.save()
            return Response(
                RoomSerializer(room).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'Bad request': 'Invalid data provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )