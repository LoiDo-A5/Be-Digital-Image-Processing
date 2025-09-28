from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from accounts.models import User
from django.contrib.auth.hashers import make_password


class RegisterPhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(min_length=10, max_length=15, source='phone_number')
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = (
            'name',
            'phone',
            'email',
            'password1',
            'password2',
            'time_zone',
        )

    def validate_phone(self, phone):
        if not phone.isdigit():
            raise serializers.ValidationError(gettext('Phone number must only contain digits'))
        return phone

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(gettext('This email is already in use'))
        return email

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(gettext("The two password fields didn't match."))

        attrs['password'] = make_password(attrs['password1'])
        attrs['username'] = attrs['phone_number']

        return attrs

    def validate_time_zone(self, time_zone):
        if not time_zone:
            time_zone = 'Asia/Ho_Chi_Minh'
        return time_zone

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class RegisterPhoneApi(GenericAPIView):
    serializer_class = RegisterPhoneSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_exists = User.objects.filter(phone_number=serializer.validated_data['phone_number']).exists()
        email_exists = User.objects.filter(email=serializer.validated_data['email']).exists()

        if phone_exists or email_exists:
            error_message = gettext('Phone number or email already exists')
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create(
            name=serializer.validated_data['name'],
            username=serializer.validated_data['phone_number'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            time_zone=serializer.validated_data.get('time_zone', 'Asia/Ho_Chi_Minh'),
        )

        return Response(
            {
                'message': gettext('Create user success'),
            }, status.HTTP_200_OK,
        )
