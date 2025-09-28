from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import serializers
import logging

from accounts.models import Message, User

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'avatar']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'timestamp']


class ListMessage(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        if room_id:
            queryset = Message.objects.filter(room_id=room_id).order_by('timestamp')
        else:
            queryset = Message.objects.none()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
