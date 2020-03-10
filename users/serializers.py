from rest_framework import serializers

from users.models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "last_name",
            "first_name",
            "email",
            "avatar",
            "superhost",
        )


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "favs",
        )


class WriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
