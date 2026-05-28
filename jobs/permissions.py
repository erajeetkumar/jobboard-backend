from rest_framework.permissions import BasePermission
from companies.models import CompanyMember
from companies.models import Company


class IsEmployerAndMember(BasePermission):

    def has_permission(self, request):

        return request.user.is_authenticated and request.user.role == "employer"

    def has_object_permission(self, request, obj):
        # obj is a Company instance
        return CompanyMember.objects.filter(user=request.user, company=obj).exists()
