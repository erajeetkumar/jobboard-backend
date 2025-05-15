
#crud serializers
from rest_framework import serializers
from .models import Company, CompanyMember


class CompanySerializer(serializers.ModelSerializer):
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
        CompanyMember.objects.create(user=user, company=company, role="owner")
        return company