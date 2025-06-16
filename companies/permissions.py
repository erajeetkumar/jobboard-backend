from rest_framework import permissions
from .models import CompanyMember

class IsCompanyAdmin(permissions.BasePermission):
    """
    Allows access only to company admins (owner or admin role).
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return (
                request.user.is_authenticated and
                getattr(request.user, 'role', None) == 'employer'
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Must be an admin or owner of the company
        return CompanyMember.objects.filter(
            user=request.user,
            company=obj,
            role__in=['admin', 'owner']
        ).exists()

class IsCompanyMember(permissions.BasePermission):
    """
    Allows access to any company member.
    """

    def has_object_permission(self, request, view, obj):
        return CompanyMember.objects.filter(
            user=request.user,
            company=obj
        ).exists()

class IsCompanyActive(permissions.BasePermission):
    """
    Allows access only if the company is active.
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_active

    def has_permission(self, request, view):
        # This permission is not used in the current views
        return True