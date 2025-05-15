from django.db import models

# Create your models here.

from django.conf import settings
from companies.models import Company

class Job(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full-time'
        PART_TIME = 'part_time', 'Part-time'
        CONTRACT = 'contract', 'Contract'
        INTERNSHIP = 'internship', 'Internship'
        TEMPORARY = 'temporary', 'Temporary'
        OTHER = 'other', 'Other'

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=200, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, related_name='jobs_posted')
    posted_at = models.DateTimeField(auto_now_add=True)
    
    application_deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    experience_level = models.CharField(max_length=100, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    skills_required = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    

    def __str__(self):
        return f"{self.title} at {self.company.name}"