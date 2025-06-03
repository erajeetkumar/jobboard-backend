# create user Registration serializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from waffle import switch_is_active

import logging

logger = logging.getLogger(__name__)
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    user = None
    
    email = serializers.EmailField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                message=_("Enter a valid email address."),
            )
        ],        
        error_messages={
            "unique": _("A user with that email already exists."),
            "invalid": _("Enter a valid email address."),
        },
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    role = serializers.ChoiceField(
        choices=[
            ("employer", "Employer"),
            ("candidate", "Job Seeker"),
            ("recruiter", "Recruiter"),
            ("hr", "HR"),
        ],
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        )

    def create(self, validated_data):
        try:
            validate_email(validated_data["email"])
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")

        try:
            
            #check if the user already exists
            if User.objects.filter(email=validated_data["email"]).exists():
                raise serializers.ValidationError(
                    "A user with this email already exists."
                )
            
            # Create the user with hashed password
            
            user = User.objects.create_user(
                email=validated_data["email"],
                password=make_password(validated_data["password"]),
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                phone_number=validated_data.get("phone_number", ""),
                role=validated_data.get("role", "candidate"),
                is_active=False,
                is_verified=False,
            )
            self.user = user
            request = self.context.get('request')
            

            # check waffle flag enforce_verification_email for email verification
            if switch_is_active( "enforce_verification_email"):
                self.send_verification_email(user)

        except Exception as e:
            if self.user:
                # If user creation failed, delete the user instance
                self.user.delete()
            
            
            logger.error(f"Error creating user: {e}")
            raise serializers.ValidationError(
                f"An error occurred while creating the user. {e}"
            )

        # logger.info(f"User created: {user.email}")
        return user

    from django.core.mail import send_mail

    def send_verification_email(self, user):
        token = RefreshToken.for_user(user).access_token
        current_site = os.getenv(
            "CURRENT_SITE", "http://localhost:8000"
        )  # Default to localhost if not set
        relative_link = f"/api/accounts/verify-email/?token={str(token)}"
        absurl = f"{current_site}{relative_link}"
        # Use Django email or external service
        print(f"Email verification link: {absurl}")

        subject = "Verify Your Email Address"
        html_content = render_to_string(
            "emails/verify_email.html", {"user": user, "verify_url": absurl}
        )

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]
        email = EmailMultiAlternatives(
            subject=subject, body=html_content, from_email=from_email, to=to_email
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
