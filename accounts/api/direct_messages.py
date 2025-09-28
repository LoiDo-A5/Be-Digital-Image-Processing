from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
import logging

from accounts.api.message_list import UserSerializer
from accounts.models import DirectMessage

logger = logging.getLogger(__name__)

class DirectMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']


class DirectMessages(ListAPIView):
    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_id = self.request.query_params.get('sender_id')
        receiver_id = self.request.query_params.get('receiver_id')

        if not sender_id or not receiver_id:
            return DirectMessage.objects.none()

        return DirectMessage.objects.filter(
            sender_id__in=[sender_id, receiver_id],
            receiver_id__in=[sender_id, receiver_id]
        ).order_by('timestamp')
