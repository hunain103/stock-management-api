from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access an object.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow staff users to access an object.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin/staff permissions
        if request.user.is_staff:
            return True
        
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
