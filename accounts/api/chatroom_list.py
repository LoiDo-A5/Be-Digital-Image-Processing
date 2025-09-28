from rest_framework import generics

from accounts.models import ChatRoom
from rest_framework import serializers
from rest_framework.generics import ListAPIView


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name']


class ChatRoomList(ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
