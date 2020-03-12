from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, "user"):
            raise Exception("해당 모델이 사용자 필드를 가지고 있지 않습니다.")
        return obj.user == request.user
