# Create your views here.

from rest_framework import viewsets, generics, status
from .models import Company, CompanyMember
from .serializers import (
    CompanyMemberSerializer,
    CompanyBaseSerializer,
    CompanyInternalSerializer,
    CompanyPublicSerializer,
)
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsCompanyAdmin, IsCompanyMember
from core.permissions import IsEmployerAndMember
from django.shortcuts import get_object_or_404

"""
Company views for handling company-related operations.
These views include listing, creating, updating, and deleting companies,
as well as managing company members.
"""

"""CompanyListCreateView: Handles listing and creating companies.
   - GET: List all companies the authenticated user is a member of.
   - POST: Create a new company (only accessible to company admins).
   - Uses CompanyInternalSerializer for serialization.
   - Requires IsAuthenticated and IsCompanyAdmin permissions."""


class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanyInternalSerializer
    permission_classes = [
        IsAuthenticated,
        IsCompanyAdmin,
    ]  # allowed to only company admins
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Company.objects.filter(members__user=self.request.user)

    def perform_create(self, serializer):

        company = serializer.save(created_by=self.request.user)


""" CompanyInternalDetail: Handles retrieving, updating, and deleting a company.
   - GET: Retrieve a company by its primary key (pk).
   - PUT/PATCH: Update a company by its primary key (pk).
   - DELETE: Delete a company by its primary key (pk).
   - Uses CompanyInternalSerializer for serialization.
   - Requires IsAuthenticated and IsCompanyAdmin permissions.
   """


class CompanyInternalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyInternalSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    lookup_field = "pk"


'''CompanyPublicDetail: Handles retrieving company details for public access.
   - GET: Retrieve a company by its slug.'''    
class CompanyPublicDetail(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyPublicSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

'''CompanyMemberListCreateView: Handles listing and creating company members.'''
class CompanyMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanyMemberSerializer
    permission_classes = [IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        company_id = self.kwargs["pk"]
        return CompanyMember.objects.filter(company__id=company_id)

    def perform_create(self, serializer):
        company = get_object_or_404(Company, pk=self.kwargs["pk"])
        if serializer.is_valid():
            serializer.save(company=company)


class CompanyMemberUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyMemberSerializer
    permission_classes = [IsAuthenticated, IsCompanyMember]
    lookup_field = "user_id"

    def get_queryset(self):
        company_id = self.kwargs["pk"]
        return CompanyMember.objects.filter(company__id=company_id)

    def get_object(self):
        company_id = self.kwargs["pk"]
        user_id = self.kwargs["user_id"]
        return get_object_or_404(
            CompanyMember, company__id=company_id, user__id=user_id
        )
