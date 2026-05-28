from django.shortcuts import render

# Create your views here.
# create a view to register users using the django rest framework
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserRegistrationSerializer, SendEmailVerificationSerializer

from logging import getLogger

logger = getLogger(__name__)
User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    View to register a new user.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def post(self, request):

        logger.info("User registration request received.")
        
        serializer = UserRegistrationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.save()
            # log the user creation

            logger.info(f"User created: {user.email}")

            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    def get(self, request):
        token = request.GET.get("token")
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response(
                {"message": "Email successfully verified."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST
            )


class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SendEmailVerificationSerializer

    @swagger_auto_schema(
        operation_description="Resend verification email to the user",
        request_body=SendEmailVerificationSerializer,
        responses={
            200: "Verification email resent successfully.",
            400: "Bad request, email is required.",
            404: "User with this email does not exist.",
        },
    )
    
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = get_user_model().objects.get(email=email)
            if user.is_verified:
                return Response(
                    {"message": "User is already verified."},
                    status=status.HTTP_200_OK,
                )
            serializer = UserRegistrationSerializer(user, context={"request": request})
            serializer.send_verification_email(user)
            return Response(
                {"message": "Verification email resent."},
                status=status.HTTP_200_OK,
            )
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
