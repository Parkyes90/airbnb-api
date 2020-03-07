from rest_framework.routers import DefaultRouter

from . import viewsets

app_name = "rooms"

router = DefaultRouter()
router.register("", viewsets.RoomViewSet, basename="room")

urlpatterns = router.urls
