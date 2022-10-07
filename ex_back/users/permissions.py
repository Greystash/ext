from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False


class IsStaffOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
                request.user.is_authenticated and (
                    request.user.is_admin or
                    request.user.is_moderator
                )
            ):
            return True
        return False
