import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rooms.models import Room
from rooms.serializers import RoomSerializer
from .serializers import UserSerializer
from .models import User
from .permissions import IsOwner


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permissions_class = [IsAdminUser]
        elif self.action in {"create", "retrieve", "favs"}:
            permissions_class = [AllowAny]
        else:
            permissions_class = [IsOwner]
        return [permission() for permission in permissions_class]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        encoded_jwt = jwt.encode(
            {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response({"token": encoded_jwt, "id": user.pk})

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomSerializer(
            user.favs.all(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        room_pk = request.data.get("pk", None)

        if room_pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(pk=room_pk)
            if request.user.favs.filter(pk=room_pk).exists():
                request.user.favs.remove(room)
            else:
                request.user.favs.add(room)
            return Response(RoomSerializer(room).data)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
