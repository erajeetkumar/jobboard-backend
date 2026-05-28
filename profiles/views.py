from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from profiles.models import JobSeekerProfile
from profiles.serializers import JobSeekerProfileSerializer
from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveUpdateAPIView

#create rest framework API view to create a candiate profile
# only one profile can be created per user
# candidate can update their profile
# no one can delete the profile

class MyJobSeekerProfileView(RetrieveUpdateAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Assumes one-to-one link: user → job seeker profile
        return self.request.user.jobseeker_profile

