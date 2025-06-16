# crud serializers
from rest_framework import serializers
from .models import Company, CompanyMember, Industry
from rest_framework.parsers import MultiPartParser, FormParser

""" Serializer for the Company model.
    - name: The name of the company (unique).
    - website: The company's website URL.
    - industry: A foreign key to the Industry model, representing the industry the company belongs to.
    - location: The location of the company.
    - description: A brief description of the company.
    - logo: The company's logo image.
    - established_year: The year the company was established.
    """
from rest_framework.exceptions import ValidationError
from waffle import flag_is_active
import logging

logger = logging.getLogger(__name__)


class CompanyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "slug", "name", "description", "logo", "location"]
        read_only_fields = ["id", "slug"]


class CompanyPublicSerializer(CompanyBaseSerializer):
    class Meta(CompanyBaseSerializer.Meta):
        pass


class CompanyInternalSerializer(CompanyBaseSerializer):
    class Meta(CompanyBaseSerializer.Meta):
        fields = CompanyBaseSerializer.Meta.fields + [
            "created_by",
            "established_year",
            "website",
            "industry",
        ]
        read_only_fields = CompanyBaseSerializer.Meta.read_only_fields + ["created_by"]

    def create(self, validated_data):

        user = self.context["request"].user
        validated_data["created_by"] = user

        logger.info(
            f"Creating company for user: {user.username} with data: {validated_data}"
        )
        # Check if the user is allowed to create a company
        logger.info(f"Checking if user {user.username} is allowed to create a company")
        logger.info(
            f"Flag 'enforce_single_company' is active: {flag_is_active(self.context['request'], 'enforce_single_company')}"
        )
        if flag_is_active(self.context["request"], "enforce_single_company"):
            if Company.objects.filter(created_by=user).exists():
                raise ValidationError("You are only allowed to create one company.")

        company = Company.objects.create(**validated_data)
        CompanyMember.objects.create(
            user=user, company=company, role="admin"
        )  # fixed role to admin
        return company

    # validate the name field to ensure it is unique
    def validate_name(self, value):
        existing_company = self.instance
        if existing_company and existing_company.name != value:            
            if Company.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    "A company with this name already exists."
                )
        return value

    # validate the website field to ensure it is unique
    #check if update is being made to the website field and if updated values is not same as existing value   
    def validate_website(self, value):
        existing_company = self.instance
        if existing_company and existing_company.website != value:
            # Check if the website already exists for another company
            if Company.objects.filter(website=value).exclude(id=existing_company.id).exists():
                raise serializers.ValidationError(
                    "A company with this website already exists."
                )
        return value


class CompanyMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = CompanyMember
        fields = ["id", "user", "user_email", "role", "joined_at"]
        read_only_fields = ["id", "user_email", "joined_at"]
