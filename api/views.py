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


class GetRoom(APIView):
    """
    API view to retrieve a room by its code.
    Inherits from APIView to define custom behavior for GET requests.
    """
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        """
        Handle GET request to retrieve a room by its code.
        Returns the room data if found, otherwise returns a 404 error.
        """
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == (
                    room[0].host
                )
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {'Room not found': 'Invalid room code.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'Bad request': 'Room code not found in request.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class JoinRoom(APIView):
    """
    API view to handle joining a room.
    Inherits from APIView to define custom behavior for POST requests.
    """
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        """
        Handle POST request to join a room using the provided code.
        Validates the room code and adds the user to the room if it exists.
        """
        if not self.request.session.exists(request.session.session_key):
            self.request.session.create()
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['room_code'] = code
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_200_OK
                )
            return Response(
                {'Bad request': 'Invalid room code.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'Bad request': 'Invalid data provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )


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
                self.request.session['room_code'] = room.code
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
                self.request.session['room_code'] = room.code
            return Response(
                RoomSerializer(room).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'Bad request': 'Invalid data provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )