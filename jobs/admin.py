from django.contrib import admin
from .models import Job

# Register your models here.


@admin.register(Job)    
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'employment_type', 'posted_by', 'posted_at', 'is_active')
    search_fields = ('title', 'company__name', 'location')
    list_filter = ('employment_type', 'is_active', 'company')
    ordering = ('-posted_at',)
   # prepopulated_fields = {'slug': ('title', 'company__name')}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'location', 'employment_type', 'company', 'posted_by')
        }),
        ('Additional Information', {
            'fields': ('application_deadline', 'experience_level', 'salary_range',
                       'skills_required', 'benefits', 'responsibilities', 'requirements')
        }),
        ('SEO Information', {
            'fields': ('slug',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )