from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin-Interface für CustomUser"""
    
    list_display = ['username', 'email', 'user_type', 'company_name', 'is_verified', 'is_staff']
    list_filter = ['user_type', 'is_verified', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'company_name', 'tax_id']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Benutzertyp & Firma', {
            'fields': ('user_type', 'company_name', 'tax_id', 'is_verified')
        }),
        ('Kontaktdaten', {
            'fields': ('phone', 'mobile')
        }),
        ('Adresse', {
            'fields': ('street', 'postal_code', 'city', 'country')
        }),
        ('Bankdaten', {
            'fields': ('iban', 'bic', 'bank_name'),
            'classes': ('collapse',)
        }),
        ('Steuerberater', {
            'fields': ('tax_advisor_name', 'tax_advisor_email'),
            'classes': ('collapse',)
        }),
        ('Notizen', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Zusätzliche Informationen', {
            'fields': ('user_type', 'email', 'company_name')
        }),
    )
