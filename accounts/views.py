from django.shortcuts import render

# Create your views here.
#create a view to register users using the django rest framework
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserRegistrationSerializer

from logging import getLogger
logger = getLogger(__name__)
User = get_user_model()

@swagger_auto_schema(request_body=UserRegistrationSerializer)
class UserRegistrationView(generics.CreateAPIView): 
    """
    View to register a new user.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = []
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            #log the user creation
            
            logger.info(f"User created: {user.email}")
            
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({'message': 'Email successfully verified.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)