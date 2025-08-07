from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for the Room model.
    Converts model instances to JSON and vice versa.
    """
    class Meta:
        """
        Meta class for RoomSerializer.
        Specifies the model and fields to be serialized.
        """
        model = Room
        fields = (
            'id',
            'code',
            'host',
            'guest_can_pause',
            'votes_to_skip',
            'created_at'
        )


class CreateRoomSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new room.
    Inherits from RoomSerializer to reuse the model fields.
    """
    class Meta:
        """
        Meta class for CreateRoomSerializer.
        Specifies the model and fields to be serialized.
        """
        model = Room
        fields = (
            'guest_can_pause',
            'votes_to_skip'
        )


class UpdateRoomSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing room.
    Inherits from RoomSerializer to reuse the model fields.
    """
    code = serializers.CharField(validators=[])
    class Meta:
        """
        Meta class for UpdateRoomSerializer.
        Specifies the model and fields to be serialized.
        """
        model = Room
        fields = (
            'guest_can_pause',
            'votes_to_skip',
            'code'
        )
