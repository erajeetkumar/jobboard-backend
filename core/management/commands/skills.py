#create command to create skills in each skill category
from django.core.management.base import BaseCommand
from core.models import Skill, SkillCategory
from django.db import transaction
from django.core.exceptions import ValidationError  

skills = {
    "Web Development": "HTML, CSS, JavaScript",
    "Data Science" : "Python, R, SQL",
    "Machine Learning" : "TensorFlow, PyTorch, Scikit-learn",
    "Mobile Development" : "React Native, Flutter, Swift",
    "Cloud Computing" : "AWS, Azure, Google Cloud",
    "DevOps" : "Docker, Kubernetes, Jenkins",
    "Cybersecurity" : "Network Security, Penetration Testing, Ethical Hacking",
    "Blockchain" : "Solidity, Ethereum, Hyperledger",
    "UI/UX Design" : "Figma, Adobe XD, Sketch",
    "Graphic Design" : "Photoshop, Illustrator, InDesign",
    "Project Management" : "Agile, Scrum, Kanban",
}

class Command(BaseCommand):
    help = "Create skills in the database"

    @transaction.atomic
    def handle(self, *args, **options):
        for category, skill_list in skills.items():
            skill_list = skill_list.split(", ")
            for skill_name in skill_list:
                skill_name = skill_name.strip()
                if not skill_name:
                    self.stdout.write(self.style.ERROR("Skill name cannot be empty."))
                    continue

                try:
                    #fetch skill category id
                    category_obj = SkillCategory.objects.get_or_create(name=category)
                    
                    skill, created = Skill.objects.get_or_create(
                        name=skill_name,
                        category=category_obj[0]  # Get the first object from the tuple returned by get_or_create,
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Skill '{skill.name}' created successfully in category '{category}'."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Skill '{skill.name}' already exists in category '{category}'."))
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f"Error creating skill '{skill_name}': {e}"))