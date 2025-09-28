from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import Friendship, User
from .login_api import UserSerializer
from ..serializers.friendship import FriendshipSerializer
from rest_framework.generics import get_object_or_404
from django.db import models
from rest_framework.decorators import action
from django.db.models import Q


class FriendshipViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(
            (models.Q(from_user=user) | models.Q(to_user=user)) & models.Q(status='accepted')
        )

    def create(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        if not to_user_id:
            return Response({'error': 'to_user_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if to_user == request.user:
            return Response({'error': 'You cannot send a friend request to yourself.'},
                            status=status.HTTP_400_BAD_REQUEST)

        existing_request = Friendship.objects.filter(
            Q(from_user=request.user, to_user=to_user) |
            Q(from_user=to_user, to_user=request.user)
        ).first()

        if existing_request:
            if existing_request.status == 'pending':
                if existing_request.to_user == request.user:
                    return Response({'error': 'There is a pending request from this user. Please accept it.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
            elif existing_request.status == 'accepted':
                return Response({'error': 'You are already friends with this user.'},
                                status=status.HTTP_400_BAD_REQUEST)

        Friendship.objects.create(from_user=request.user, to_user=to_user, status='pending')
        return Response({'message': 'Friend request sent successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def cancel_request(self, request):
        to_user_id = request.data.get('to_user_id')
        if not to_user_id:
            return Response({"error": "to_user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        friendship = Friendship.objects.filter(from_user=request.user, to_user_id=to_user_id, status='pending').first()

        if not friendship:
            return Response({"error": "Friendship request not found or not pending."}, status=status.HTTP_404_NOT_FOUND)

        friendship.delete()
        return Response({"message": "Friendship request cancelled."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def friends_list(self, request):
        friendships = Friendship.objects.filter(
            Q(from_user=request.user, status='accepted') | Q(to_user=request.user, status='accepted')
        )

        friends = [
            friendship.to_user if friendship.from_user == request.user else friendship.from_user
            for friendship in friendships
        ]

        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def incoming_requests(self, request):
        incoming_friendships = Friendship.objects.filter(to_user=request.user, status='pending')
        requesters = [fs.from_user for fs in incoming_friendships]
        serializer = UserSerializer(requesters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def accept_request(self, request):
        from_user_id = request.data.get('from_user_id')
        if not from_user_id:
            return Response({'error': 'from_user_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_user = User.objects.get(id=from_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User who sent the request not found.'}, status=status.HTTP_404_NOT_FOUND)

        friendship = Friendship.objects.filter(
            from_user=from_user, to_user=request.user, status='pending'
        ).first()

        if not friendship:
            return Response({'error': 'Friend request not found or already accepted/rejected.'},
                            status=status.HTTP_404_NOT_FOUND)

        friendship.status = 'accepted'
        friendship.save()

        return Response({'message': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'], url_path='remove-friend')
    # def remove_friend(self, request):
    #     user_id = request.data.get('user_id')
    #     friendship = Friendship.objects.filter(
    #         (Q(from_user=request.user, to_user_id=user_id) | Q(to_user=request.user, from_user_id=user_id)),
    #         status='accepted'
    #     ).first()
    #
    #     if not friendship:
    #         return Response({"error": "Friendship not found."}, status=status.HTTP_404_NOT_FOUND)
    #
    #     friendship.status = 'removed'
    #     friendship.save()
    #     return Response({"message": "Friend removed."}, status=status.HTTP_200_OK)