from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
SAFE_METHODS_FOR_FAVORITE = ('POST', 'DELETE', 'HEAD', 'OPTIONS')


class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )


class IsAuthenticatedForQuestionFavorite(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS_FOR_FAVORITE or
            request.user and
            request.user.is_authenticated
        )
