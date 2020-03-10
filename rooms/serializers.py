from rest_framework import serializers

from rooms.models import Room
from users.serializers import RelatedUserSerializer


class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class WriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "name",
            "address",
            "price",
            "beds",
            "lat",
            "lng",
            "bedrooms",
            "bathrooms",
            "check_in",
            "check_out",
            "instant_book",
        )

    def validate(self, data):
        if not self.instance:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        else:
            check_in = self.instance.check_in
            check_out = self.instance.check_out
        if check_in == check_out:
            raise serializers.ValidationError(
                "Not enough time between changes"
            )
        return data
