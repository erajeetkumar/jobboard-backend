# Create your views here.

from rest_framework import viewsets
from .models import Company, CompanyMember
from .serializers import CompanySerializer
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated

from django.shortcuts import render

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


#employer views
# can create one company
# can update and delete their own company
# can add additional members to their company

''' create a viewset for the company model
    - list all companies
    - create a new company
    - retrieve a company
    - update a company
    - delete a company
'''
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsEmployerAndMember]

    def get_queryset(self):
        return Company.objects.filter(members__user=self.request.user)
