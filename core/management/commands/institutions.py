#create command to insert institutions
from django.core.management.base import BaseCommand
from core.models import Institution
from django.db import transaction
from django.core.exceptions import ValidationError
institutions = [
    "Harvard University",
    "Stanford University",
    "Massachusetts Institute of Technology (MIT)",
    "California Institute of Technology (Caltech)",
    "University of Oxford",
    "University of Cambridge",
    "University of Chicago",
    "Imperial College London",
    "ETH Zurich - Swiss Federal Institute of Technology",
    "University College London (UCL)",
]
class Command(BaseCommand):
    help = "Create institutions in the database"
    
    @transaction.atomic
    def handle(self, *args, **options):
        
        for institution_name in institutions:
            institution_name = institution_name.strip()
            if not institution_name:
                self.stdout.write(self.style.ERROR("Institution name cannot be empty."))
                continue

            try:
                institution, created = Institution.objects.get_or_create(
                    name=institution_name,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Institution '{institution.name}' created successfully."))
                else:
                    self.stdout.write(self.style.WARNING(f"Institution '{institution.name}' already exists."))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f"Error creating institution '{institution_name}': {e}"))