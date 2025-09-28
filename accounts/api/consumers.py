import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import logging
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import ChatRoom, Message, DirectMessage

logger = logging.getLogger(__name__)
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_type = self.scope['url_route']['kwargs']['chat_type']
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        if self.chat_type == "dm":
            sender_id, receiver_id = map(int, self.room_id.split('_'))
            self.room_group_name = f"dm_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
        else:
            self.room_group_name = f"{self.chat_type}_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        if self.chat_type == "room":
            user = await self.save_room_message(sender_id, message)
        else:  # chat_type == "dm"
            receiver_id = data['receiver_id']
            user = await self.save_direct_message(sender_id, receiver_id, message)

        if user:
            user_info = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'avatar': user.avatar.url if user.avatar and hasattr(user.avatar, 'url') else None
            }
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user_info
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        await self.send(text_data=json.dumps({'message': message, 'user': user}))

    @database_sync_to_async
    def save_room_message(self, sender_id, content):
        try:
            user = User.objects.get(id=sender_id)
            room = ChatRoom.objects.get(id=self.room_id)
            Message.objects.create(room=room, sender=user, content=content, timestamp=timezone.now())
            return user
        except ObjectDoesNotExist as e:
            logger.error(f"Error saving room message: {e}")
            return None

    @database_sync_to_async
    def save_direct_message(self, sender_id, receiver_id, content):
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            DirectMessage.objects.create(sender=sender, receiver=receiver, content=content, timestamp=timezone.now())
            return sender
        except ObjectDoesNotExist as e:
            logger.error(f"Error saving direct message: {e}")
            return None