from rest_framework import permissions


class IsAdminOrObjectOwnerToRead(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are
     - owner may GET, PUT, POST, DELETE
     - nobody else can access
     """

    def has_object_permission(self, request, view, obj):
        # check if super user
        if request.user.is_superuser:
            return True
        # check if user is owner
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.user
