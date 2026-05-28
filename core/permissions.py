
from companies.models import CompanyMember
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated

class IsEmployerAndMember(BasePermission):
    """
    - Only employers can create a company.
    - Only company members can view/update.
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated and request.user.role == 'employer'
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj is a Company instance
        return CompanyMember.objects.filter(user=request.user, company=obj).exists()