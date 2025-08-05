from django.db import models

import random
import string


def generate_unique_code():
    """
    Generates a unique code for the room.
    The code consists of 8 uppercase letters and digits.
    """
    length = 8

    while True:
        # Generate a random code
        code = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=length
            )
        )
        # Check if the code is unique
        # If the code is not unique, generate a new one
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


class Room(models.Model):
    """
    Represents a room in the house party.
    """
    code = models.CharField(
        max_length=8,
        default=generate_unique_code,
        unique=True
    )
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure the code is unique.
        If the code is empty, generate a new unique code.
        """
        if self.code == '':
            self.code = generate_unique_code()
        super().save(*args, **kwargs)