#create command to create degrees
#         verbose_name = "Degree"
#         verbose_name_plural = "Degrees"
#         ordering = ["name"]
from django.core.management.base import BaseCommand
from core.models import Degree
from django.db import transaction
from django.utils.text import slugify
from django.core.exceptions import ValidationError

degrees  = [
    "B.A. (Bachelor of Arts)",
    "B.Sc. (Bachelor of Science)",
    "B.Com. (Bachelor of Commerce)",
    "B.E. (Bachelor of Engineering)",
    "B.Tech (Bachelor of Technology)",
    "BBA (Bachelor of Business Administration)",
    "MBA (Master of Business Administration)",
    "M.A. (Master of Arts)",
    "M.Sc. (Master of Science)",
    "M.Com. (Master of Commerce)",
    "M.E. (Master of Engineering)",
    "M.Tech (Master of Technology)",
    "Ph.D. (Doctor of Philosophy)",
    "M.Phil. (Master of Philosophy)",
    "LL.B. (Bachelor of Laws)",
    "LL.M. (Master of Laws)",
    "B.Ed. (Bachelor of Education)",    
]
class Command(BaseCommand):
    help = "Create degrees in the database"
    
    @transaction.atomic
    def handle(self, *args, **options):
        
        for degree_name in degrees:
            degree_name = degree_name.strip()
            if not degree_name:
                self.stdout.write(self.style.ERROR("Degree name cannot be empty."))
                continue

            try:
                degree, created = Degree.objects.get_or_create(
                    name=degree_name,
                    
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Degree '{degree.name}' created successfully."))
                else:
                    self.stdout.write(self.style.WARNING(f"Degree '{degree.name}' already exists."))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f"Error creating degree '{degree_name}': {e}"))


#insert sample degrees
