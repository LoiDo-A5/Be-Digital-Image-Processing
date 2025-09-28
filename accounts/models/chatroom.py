from django.db import models

from accounts.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')

    def __str__(self):
        return self.name
