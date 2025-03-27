from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "user":
            return obj.assigned_to == request.user
        
        return False
