from django.shortcuts import render
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated
from companies.models import Company, CompanyMember

from .models import Job
from .serializers import JobSerializer
from rest_framework import viewsets

# Create your views here.

class IsEmployerAndMember(BasePermission):
   
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated and request.user.role == 'employer'
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj is a Company instance
        return CompanyMember.objects.filter(user=request.user, company=obj).exists()


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployerAndMember]

    