# Create your views here.

from rest_framework import viewsets
from .models import Company, CompanyMember
from .serializers import CompanySerializer, CompanyMemberSerializer
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser

from core.permissions import IsEmployerAndMember


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

@swagger_auto_schema(request_body=CompanySerializer)
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsEmployerAndMember]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        return Company.objects.filter(members__user=self.request.user)


''' create a viewset for the company member model
    - list all company members
    - create a new company member
    - retrieve a company member
    - update a company member
    - delete a company member
'''
class CompanyMemberViewSet(viewsets.ModelViewSet):
    queryset = CompanyMember.objects.all()
    serializer_class = CompanyMemberSerializer
    permission_classes = [IsAuthenticated, IsEmployerAndMember]

    def get_queryset(self):
        return CompanyMember.objects.filter(user=self.request.user)