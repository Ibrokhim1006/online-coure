from rest_framework.permissions import BasePermission, IsAuthenticated


class IsTeacher(BasePermission):
    """Rights only for admin"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.groups.filter(name='teacher').exists() )
    

class IsLogin(BasePermission):
    """Rights only for Login"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated)


class IsStudent(BasePermission):
    """Rights only for user"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.groups.filter(name='studdent').exists() )