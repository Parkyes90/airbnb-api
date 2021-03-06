import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            prefix, jwt_token = token.split(" ")
            decoded = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            pk = decoded.get("pk")
            user = User.objects.get(pk=pk)
            return user, None
        except (
            ValueError,
            jwt.exceptions.DecodeError,
            User.DoesNotExist,
            AttributeError,
        ):
            return None
