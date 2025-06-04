from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission 
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager

from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password( password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



# Create your models here
class User(AbstractUser):
    """
    Custom user model that extends the AbstractUser model.
    """
    
    class Role(models.TextChoices):
        CANDIDATE = 'candidate', 'Candidate'
        EMPLOYER = 'employer', 'Employer'
        ADMIN = 'administrator', 'Administrator'
        RECRUITER = 'recruiter', 'Recruiter'
        HR = 'hr', 'HR'
        
        
    # Add any additional fields you want to include in your custom user model
    # For example, you can add a profile picture field:
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    
    #social media links
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    
    #social providers
    social_provider = models.CharField(max_length=255, blank=True, null=True)
    #social provider id
    social_provider_id = models.CharField(max_length=255, blank=True, null=True)
    # Add any additional fields you want to include in your custom user model
    
    #two factor authentication
    two_factor_auth = models.BooleanField(default=False)
    

    email = models.EmailField(unique=True)
    
    objects = CustomUserManager()
    # Override the username field to use email instead
    username = None
    USERNAME_FIELD = 'email'
    
    phone_number = models.CharField(
        max_length=17,
        blank=True,
        null=True
        
    )
    
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    role= models.CharField(
        max_length=100,
        choices=Role.choices,
        default=Role.CANDIDATE,
    )
    
    
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )
    
    is_verified = models.BooleanField(default=False, help_text=_('Indicates whether the user has verified their email address.'))
    
    def __str__(self):
        return self.get_full_name()
    
    # You can also add any additional methods you want to include in your custom user model