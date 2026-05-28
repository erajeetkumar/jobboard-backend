from django.contrib import admin

from .models import JobSeekerProfile, Education, UserSkill, Experience

# Register your models here.
admin.site.register(
    [
        JobSeekerProfile,
        Education,
        UserSkill,
        Experience,  # Assuming Experience model is defined in profiles/models.py
    ]
)
