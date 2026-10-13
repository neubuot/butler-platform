from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
import csv
from django.http import HttpResponse


def export_users_to_csv(modeladmin, request, queryset):
    """Exportiert ausgewählte Benutzer als CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="benutzer_export.csv"'
    response.write('\ufeff')  # UTF-8 BOM für Excel
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Benutzername', 'E-Mail', 'Benutzertyp', 'Firmenname', 
        'Telefon', 'Stadt', 'Verifiziert', 'Erstellt am'
    ])
    
    for user in queryset:
        writer.writerow([
            user.username,
            user.email,
            user.get_user_type_display(),
            user.company_name or '',
            user.phone or '',
            user.city or '',
            'Ja' if user.is_verified else 'Nein',
            user.created_at.strftime('%d.%m.%Y')
        ])
    
    return response

export_users_to_csv.short_description = "Ausgewählte Benutzer als CSV exportieren"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin-Interface für CustomUser"""
    
    list_display = ['username', 'email', 'user_type', 'company_name', 'is_verified', 'is_staff']
    list_filter = ['user_type', 'is_verified', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'company_name', 'tax_id']
    actions = [export_users_to_csv]
    
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