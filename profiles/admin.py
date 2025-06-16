from django.contrib import admin

from .models import JobSeekerProfile, Education, UserSkill

# Register your models here.
admin.site.register(
    [
        JobSeekerProfile,
        Education,
        UserSkill,
    ]
)
