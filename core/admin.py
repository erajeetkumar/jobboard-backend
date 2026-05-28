from django.contrib import admin

# Register your models here.
from .models import Institution, Degree, FieldOfStudy, JobType, Skill, SkillCategory

admin.site.register([
    # Add your models here
    Institution,
    Degree,
    FieldOfStudy,
    JobType,
    Skill,
    SkillCategory,
])
