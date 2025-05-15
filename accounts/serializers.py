#create user Registration serializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.core.validators import validate_email

from .models import User

import logging
logger = logging.getLogger(__name__)
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    email = serializers.EmailField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message=_("Enter a valid email address.")
            )
        ]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    
    role = serializers.ChoiceField(
        choices=[
            ('employer', 'Employer'),
            ('candidate', 'Job Seeker')
        ],
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'role')
        
    def create(self, validated_data):
        try:
            validate_email(validated_data['email'])
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")

        try:
            user = User.objects.get(email=validated_data['email'])
            if user.is_employer:
                raise serializers.ValidationError("Email already exists.")
        except User.DoesNotExist:
            pass
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise serializers.ValidationError("An error occurred while creating the user.")

        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                password= make_password(validated_data['password']),
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                phone_number=validated_data.get('phone_number', ''),
                role=validated_data.get('role', 'candidate')
            )
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise serializers.ValidationError("An error occurred while creating the user.")

        logger.info(f"User created: {user.email}")
        return user  