from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'avatar', 'phone_number', 'birthday')


class UserListApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
