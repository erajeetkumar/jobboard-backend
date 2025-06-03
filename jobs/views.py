from django.shortcuts import render
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from companies.models import Company, CompanyMember
from .permissions import IsEmployerAndMember
from .models import Job
from .serializers import JobSerializer
from rest_framework import viewsets

# Create your views here.
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        self.user = self.request.user
        
        if self.action in ("create", "update"):
            return [IsEmployerAndMember]  # Require admin for create/update
        return super().get_permissions()  # Use default permissions for other actions

