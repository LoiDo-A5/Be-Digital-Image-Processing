from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User


class MeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def update(self, instance, validated_data):
        user = instance
        user.name = validated_data['name']
        user.save()
        return user


class MePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name', 'email', 'avatar', 'phone_number',
            'birthday',
        )


class MeApi(GenericAPIView):
    serializer_class = MeSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return MePatchSerializer
        return super().get_serializer_class()

    def get(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.get_serializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request):
        serializer = self.get_serializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
