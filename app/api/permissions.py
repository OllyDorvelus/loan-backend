from rest_framework import permissions


class IsAdminOrObjectOwnerToRead(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are
     - owner may GET, PUT, POST, DELETE
     - nobody else can access
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # check if super user
        if request.user.is_superuser:
            return True
        # check if user is owner
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.user
        return False


class AuthenticatedCantPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.method == "POST"
            and request.user.is_authenticated
            and not request.user.is_superuser
        ):
            return False
        return True


class IsAdminOrObjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return request.user.is_authenticated
        return request.user.is_superuser or request.user == obj.user


class IsAdminOrUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj


class IsAdminOrUserOwnerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_superuser = request.user.is_superuser
        if request.method in permissions.SAFE_METHODS:
            return is_superuser or request.user == obj.user
        return is_superuser
