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
        read_only_fields = ('id', 'created_at')