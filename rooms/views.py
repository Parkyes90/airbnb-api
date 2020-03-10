from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room
from .serializers import RoomSerializer


class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(status=status.HTTP_200_OK, data=serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )

        room = serializer.save()
        return Response(
            status=status.HTTP_200_OK, data=RoomSerializer(room).data
        )

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if room is not None:
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
