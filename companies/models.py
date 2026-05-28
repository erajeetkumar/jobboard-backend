from django.db import models

# Create your models here.

from django.conf import settings
from django.utils.text import slugify

'''
This module defines the models for the companies app, including:
- Industry: Represents different industries.
- Company: Represents a company with various attributes.
- CompanyMember: Represents a member of a company with a specific role.'''


'''
Industry Model:
- name: The name of the industry (unique).
- description: A brief description of the industry.'''
class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Industries'
        unique_together = ('name',)
        
    
    def __str__(self):
        return self.name
    

'''Company Model:
- name: The name of the company (unique).
- website: The company's website URL.
- industry: A foreign key to the Industry model, representing the industry the company belongs to.
- location: The location of the company.
- description: A brief description of the company.
- logo: The company's logo image.
- established_year: The year the company was established.
'''
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='companies', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_companies', null=True, blank=True)
    
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Companies'
        unique_together = ('name', 'website')
        
    def __str__(self):
        return self.name

'''
CompanyMember Model: This model represents a member of a company with a specific role.

- user: A foreign key to the User model, representing the user who is a member of the company.
- company: A foreign key to the Company model, representing the company the user belongs to.
- role: The role of the user in the company (e.g., admin, recruiter).
- joined_at: The date and time when the user joined the company.

'''
class CompanyMember(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        RECRUITER = 'recruiter', 'Recruiter'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='company_memberships')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.RECRUITER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'company')
        ordering = ['-joined_at']
        verbose_name_plural = 'Company Members'
        verbose_name = 'Company Member'
        

    def __str__(self):
        return f"{self.user.email} as {self.role} in {self.company.name}"