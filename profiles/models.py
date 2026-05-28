from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.core.signing import TimestampSigner


'''Job Seeker Profile Model
This module represents a job seeker's profile, including resume.
'''
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobseeker_profile",
    )
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    #skills = models.TextField(blank=True, help_text="Comma-separated skills")
    github = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    headline = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="A short headline or summary of your professional profile",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.email
    
    
    


from core.models import Institution, Degree
from core.models import FieldOfStudy  # Assuming FieldOfStudy is defined in core.models

'''Education Model
This model represents the education details of a job seeker, including institution, degree, field of study, and dates attended.'''
class Education(models.Model):
    profile = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="education"
    )
    institution = models.ForeignKey(
        "core.Institution", on_delete=models.CASCADE, related_name="education", null=True, blank=True
    )
    institution_name = models.CharField(max_length=255, blank=True, null=True)

    degree = models.ForeignKey(
        "core.Degree", on_delete=models.CASCADE, related_name="education", null=True, blank=True
    )

    field_of_study = models.ForeignKey(
        "core.FieldOfStudy",
        on_delete=models.CASCADE,
        related_name="education",
        blank=True,
        null=True,
    )
    field_of_study_name = models.CharField(max_length=255, blank=True, null=True)
    degree_name = models.CharField(max_length=255, blank=True, null=True)
    degree_description = models.TextField(blank=True, null=True)

    start_at = models.DateField()
    end_at = models.DateField(blank=True, null=True)

    still_studying = models.BooleanField(
        default=False, help_text="Check if still studying"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"
        ordering = ["-start_at"]

    
    def save(self, *args, **kwargs):
        if self.institution:
            self.institution_name = self.institution.name
        if self.degree:
            self.degree_name = self.degree.name
            self.degree_description = self.degree.description
        if self.field_of_study:
            self.field_of_study_name = self.field_of_study.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

'''Experience Model
This model represents the work experience of a job seeker, including company name, job title, dates worked, responsibilities, and whether they are still employed there.'''

class Experience(models.Model):
    profile = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="experience"
    )
    company_name = models.CharField(max_length=255)
    company = models.ForeignKey("companies.Company", on_delete=models.SET_NULL, related_name="experience", null=True, blank=True)
    
    job_title = models.CharField(max_length=255)
    joined_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    responsibilites = models.TextField(blank=True, max_length=5000)
    still_working = models.BooleanField(
        default=False, help_text="Check if currently working here"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return f"{self.job_title} at {self.company}"

'''User Skill Model
This model represents a skill possessed by a job seeker, including the skill name, level, and associated profile. It can be linked to a predefined skill from the core app.'''
class UserSkill(models.Model):
    profile = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="user_skills"
    )
    skill = models.ForeignKey(
        "core.Skill", on_delete=models.SET_NULL, related_name="main_skills", null=True, blank=True
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Skill"
        verbose_name_plural = "User Skills"
        ordering = ["skill__name"]

    def save(self, *args, **kwargs):
        if self.skill:
            self.name = self.skill.name
        super().save(*args, **kwargs)
        self.name = self.name.strip() if self.name else None
        if not self.name:
            raise ValueError("Skill name cannot be empty.")

    def __str__(self):
        return self.name

'''Certification Model
This model represents a certification obtained by a job seeker, including details such as the name, issuer, issue date, expiration date, and certificate URL.
a document field is included to upload the certification document.'''

class Certification(models.Model):
    profile = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="certifications"
    )
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    certificate_url = models.URLField(blank=True, null=True)
    certificate_number = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text="Description of the certification")
    document = models.FileField(
        upload_to="certifications/",
        blank=True,
        null=True,
        help_text="Upload the certification document",
        
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ["-issue_date"]

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError("Certification name cannot be empty.")
        super().save(*args, **kwargs)
        self.name = self.name.strip()

    def __str__(self):
        return self.name

User = settings.AUTH_USER_MODEL

'''Profile View Model
This model tracks views of job seeker profiles by users, including the viewer, candidate, and metadata about the view.
'''
class ProfileView(models.Model):
    viewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profile_views'
    )
    candidate = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name='views'
    )
    viewed_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100, blank=True, null=True)  # e.g., 'job_app', 'search'
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["candidate", "viewed_at"]),
            models.Index(fields=["viewer", "viewed_at"]),
        ]
