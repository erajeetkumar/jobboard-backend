#create serializers for the profiles app
from rest_framework import serializers
from profiles.models import JobSeekerProfile, Education, Experience, UserSkill


# education
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'degree', 'institution', 'field_of_study', 'start_at', 'end_at', 'still_studying', 'degree_name', 'institution_name', 'field_of_study_name', 'degree_description']

# experience
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'job_title', 'company', 'joined_date', 'end_date', 'responsibilites', 'company_name', 'still_working']

# skill
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ['id', 'name', 'level']  # Optional proficiency level

from django.core.signing import Signer, TimestampSigner

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    experience = ExperienceSerializer(many=True)
    user_skills = SkillSerializer(many=True)
    token = serializers.SerializerMethodField()
    class Meta:
        model = JobSeekerProfile
        fields = [                  
            'headline',
            'location',           
            'bio',           
            'education',
            'experience',
            'user_skills',
            'token'
        ]       

    
    def get_token(self, obj):
        signer = TimestampSigner()
        return signer.sign(str(obj.id) )
    
    def create(self, validated_data):
        education_data = validated_data.pop('education', [])
        experience_data = validated_data.pop('experience', [])
        skills_data = validated_data.pop('user_skills', [])

        profile = JobSeekerProfile.objects.create(**validated_data)

        for edu in education_data:
            Education.objects.create(profile=profile, **edu)

        for exp in experience_data:
            Experience.objects.create(profile=profile, **exp)

        for skill in skills_data:
            UserSkill.objects.create(profile=profile, **skill)

        return profile

    def update(self, instance, validated_data):
        education_data = validated_data.pop('education', [])
        experience_data = validated_data.pop('experience', [])
        skills_data = validated_data.pop('user_skills', [])

        # update base fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Option A: delete & recreate (simple)
        instance.education.all().delete()
        instance.experience.all().delete()
        instance.user_skills.all().delete()

        for edu in education_data:
            Education.objects.create(profile=instance, **edu)
        for exp in experience_data:
            Experience.objects.create(profile=instance, **exp)
        for skill in skills_data:
            UserSkill.objects.create(profile=instance, **skill)

        return instance
