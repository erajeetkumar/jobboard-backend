from django.contrib import admin

# Register company models in the admin site
from .models import Company, Industry, CompanyMember

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'slug', 'industry', 'location', 'is_verified', 'is_active')
    search_fields = ('name', 'website', 'industry__name')
    list_filter = ('is_verified', 'is_active', 'industry')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Company, CompanyAdmin)

class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    #prepopulated_fields = {'slug': ('name',)}
admin.site.register(Industry, IndustryAdmin)
class CompanyMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role', 'joined_at')
    search_fields = ('user__email', 'company__name', 'role')
    list_filter = ('role',)
    ordering = ('-joined_at',)
    #prepopulated_fields = {'slug': ('name',)}
admin.site.register(CompanyMember, CompanyMemberAdmin)
