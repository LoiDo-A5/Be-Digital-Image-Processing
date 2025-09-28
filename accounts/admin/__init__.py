from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy

from accounts.admin.chatroom_admin import ChatRoomAdmin
from accounts.admin.direct_message_admin import DirectMessageAdmin
from accounts.admin.friendship_admin import FriendShipAdmin
from accounts.admin.message_admin import MessageAdmin
from accounts.admin.token_admin import FilterTokenAdmin
from accounts.admin.user_admin import UserAdmin
from accounts.models import User, ChatRoom, Message, DirectMessage, Friendship

admin.site.register(User, UserAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(DirectMessage, DirectMessageAdmin)
admin.site.register(Friendship, FriendShipAdmin)

admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, FilterTokenAdmin)
