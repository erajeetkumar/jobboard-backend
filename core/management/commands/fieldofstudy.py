#create command to create fields of study
from django.core.management.base import BaseCommand
from core.models import FieldOfStudy
from django.db import transaction
from django.core.exceptions import ValidationError
fields_of_study = [
    "Computer Science",
    "Information Technology",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Biotechnology",
    "Business Administration",
    "Economics",
    "Psychology",
    "Sociology",
    "Political Science",
    "Environmental Science",
    "Mathematics",
    "Physics",
    "Chemistry",
]
class Command(BaseCommand):
    help = "Create fields of study in the database"
    
    @transaction.atomic
    def handle(self, *args, **options):
        
        for field_name in fields_of_study:
            field_name = field_name.strip()
            if not field_name:
                self.stdout.write(self.style.ERROR("Field of study name cannot be empty."))
                continue

            try:
                field_of_study, created = FieldOfStudy.objects.get_or_create(
                    name=field_name,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Field of Study '{field_of_study.name}' created successfully."))
                else:
                    self.stdout.write(self.style.WARNING(f"Field of Study '{field_of_study.name}' already exists."))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f"Error creating field of study '{field_name}': {e}"))