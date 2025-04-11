from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin').exists()

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='user').exists()

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only methods (GET, etc.)
        return request.user.groups.filter(name='admin').exists()