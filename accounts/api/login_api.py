from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TokenLoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()


class LoginApi(GenericAPIView):
    serializer_class = TokenLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self._authenticate_user(request, **serializer.validated_data)

        if not user:
            return Response(
                {
                    'message': gettext('Incorrect username or password'),
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        # Tạo access và refresh tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        user_data = UserSerializer(user).data

        return Response(
            {
                'access': access,
                'refresh': str(refresh),
                'user': user_data,
            },
            status=status.HTTP_200_OK
        )

    def _authenticate_user(self, request, **kwargs):
        user = authenticate(request, **kwargs)
        return user
