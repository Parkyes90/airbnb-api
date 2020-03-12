from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import Room
from .permissions import IsOwner
from .serializers import RoomSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        max_price = request.GET.get("max_price", None)
        min_price = request.GET.get("min_price", None)
        beds = request.GET.get("bedrooms", None)
        bathrooms = request.GET.get("bathrooms", None)
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)
        filter_kwargs = {}
        paginator = self.paginator
        try:
            if max_price is not None:
                filter_kwargs["price__lte"] = max_price
            if min_price is not None:
                filter_kwargs["price__gte"] = min_price
            if beds is not None:
                filter_kwargs["beds__gte"] = beds
            if bathrooms is not None:
                filter_kwargs["bathrooms__gte"] = bathrooms
            if lat is not None and lng is not None:
                filter_kwargs["lat_gte"] = float(lat) - 0.005
                filter_kwargs["lat_lte"] = float(lat) + 0.005
                filter_kwargs["lng_gte"] = float(lng) - 0.005
                filter_kwargs["lng_lte"] = float(lng) + 0.005
            rooms = Room.objects.filter(**filter_kwargs)
        except ValueError:
            rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
