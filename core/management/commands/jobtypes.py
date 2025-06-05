#create command to create job types
from django.core.management.base import BaseCommand
from core.models import JobType
from django.db import transaction
from django.core.exceptions import ValidationError
job_types = [
    "Full-time",
    "Part-time",
    "Contract",
    "Temporary",
    "Internship",
    "Freelance",
    "Remote",
    "On-site",
    "Hybrid",
]
class Command(BaseCommand):
    help = "Create job types in the database"
    
    @transaction.atomic
    def handle(self, *args, **options):
        
        for job_type_name in job_types:
            job_type_name = job_type_name.strip()
            if not job_type_name:
                self.stdout.write(self.style.ERROR("Job type name cannot be empty."))
                continue

            try:
                job_type, created = JobType.objects.get_or_create(
                    name=job_type_name,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Job Type '{job_type.name}' created successfully."))
                else:
                    self.stdout.write(self.style.WARNING(f"Job Type '{job_type.name}' already exists."))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f"Error creating job type '{job_type_name}': {e}"))