
#crud serializers
from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'posted_at', 'posted_by', 'is_active', 'company']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'location': {'required': True},
            'employment_type': {'required': True},
            
        }
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['posted_by'] = user
        validated_data['company'] = user.created_companies.first()
        job = Job.objects.create(**validated_data)
        return job
    
    