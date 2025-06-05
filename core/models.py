from django.db import models

# Create your models here.
# create institution model


class Institution(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Degree"
        verbose_name_plural = "Degrees"
        ordering = ["name"]

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Field of Study"
        verbose_name_plural = "Fields of Study"
        ordering = ["name"]

    def __str__(self):
        return self.name


class JobType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Job Type"
        verbose_name_plural = "Job Types"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class SkillCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        SkillCategory, on_delete=models.CASCADE, related_name="skills"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ["name"]

    def __str__(self):
        return self.name