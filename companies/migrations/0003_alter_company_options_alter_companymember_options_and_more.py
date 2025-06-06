# Generated by Django 5.2.1 on 2025-05-20 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_alter_industry_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='companymember',
            options={'ordering': ['-joined_at'], 'verbose_name': 'Company Member', 'verbose_name_plural': 'Company Members'},
        ),
        migrations.AlterModelOptions(
            name='industry',
            options={'ordering': ['name'], 'verbose_name_plural': 'Industries'},
        ),
        migrations.AddField(
            model_name='industry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='company',
            unique_together={('name', 'website')},
        ),
        migrations.AlterUniqueTogether(
            name='industry',
            unique_together={('name',)},
        ),
    ]
