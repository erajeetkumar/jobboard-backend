from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import JobSeekerProfile

import logging
Logger = logging.getLogger(__name__)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_jobseeker_profile(sender, instance, created, **kwargs):
    # Ensure the user is a job seeker before creating the profile
    if created and instance.role == 'candidate':        
        JobSeekerProfile.objects.create(user=instance)
        Logger.info(f"Created JobSeekerProfile for user {instance.email}")


