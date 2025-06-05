#create command to create skill categories
from django.core.management.base import BaseCommand
from core.models import SkillCategory
from django.db import transaction
from django.core.exceptions import ValidationError
skill_categories = [
    "Programming Languages",
    "Web Development",
    "Mobile Development",
    "Data Science",
    "Machine Learning",
    "Artificial Intelligence",
    "Cloud Computing",
    "DevOps",
    "Cybersecurity",
    "Blockchain",
    "UI/UX Design",
    "Graphic Design",
    "Project Management",
]
class Command(BaseCommand):
    help = "Create skill categories in the database"
    
    @transaction.atomic
    def handle(self, *args, **options):
        
        for category_name in skill_categories:
            category_name = category_name.strip()
            if not category_name:
                self.stdout.write(self.style.ERROR("Skill category name cannot be empty."))
                continue

            try:
                skill_category, created = SkillCategory.objects.get_or_create(
                    name=category_name,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Skill Category '{skill_category.name}' created successfully."))
                else:
                    self.stdout.write(self.style.WARNING(f"Skill Category '{skill_category.name}' already exists."))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f"Error creating skill category '{category_name}': {e}"))