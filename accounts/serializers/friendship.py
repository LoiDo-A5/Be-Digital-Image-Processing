from rest_framework import serializers

from accounts.models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    from_user_name = serializers.CharField(source='from_user.username', read_only=True)
    to_user_name = serializers.CharField(source='to_user.username', read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'from_user_name', 'to_user_name', 'status', 'created_at']
