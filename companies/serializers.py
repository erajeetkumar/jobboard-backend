
#crud serializers
from rest_framework import serializers
from .models import Company, CompanyMember, Industry
from rest_framework.parsers import MultiPartParser, FormParser

''' Serializer for the Company model.
    - name: The name of the company (unique).
    - website: The company's website URL.
    - industry: A foreign key to the Industry model, representing the industry the company belongs to.
    - location: The location of the company.
    - description: A brief description of the company.
    - logo: The company's logo image.
    - established_year: The year the company was established.
    '''
class CompanySerializer(serializers.ModelSerializer):
    
    logo = serializers.ImageField(required=False, allow_null=True)
    industry = serializers.PrimaryKeyRelatedField(
        queryset=Industry.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'is_verified', 'is_active']
        extra_kwargs = {
            'name': {'required': True},           
        }
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        company = Company.objects.create(**validated_data)
        CompanyMember.objects.create(user=user, company=company, role="admin") #fixed role to admin
        return company
    
    #validate the name field to ensure it is unique
    def validate_name(self, value):
        if Company.objects.filter(name=value).exists():
            raise serializers.ValidationError("A company with this name already exists.")
        return value
    #validate the website field to ensure it is unique
    def validate_website(self, value):
        if Company.objects.filter(website=value).exists():
            raise serializers.ValidationError("A company with this website already exists.")
        return value
    

# Serializer for the CompanyMember model.
class CompanyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMember
        fields = '__all__'
        read_only_fields = ['id', 'joined_at']
        extra_kwargs = {
            'user': {'required': True},
            'company': {'required': True},
            'role': {'required': True},
        }