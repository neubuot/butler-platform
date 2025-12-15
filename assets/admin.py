from django.contrib import admin
from .models import ButlerDevice, MaintenanceRecord
import csv
from django.http import HttpResponse


def export_devices_to_csv(modeladmin, request, queryset):
    """Exportiert ausgewählte Butler-Geräte als CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="butler_geraete_export.csv"'
    response.write('\ufeff')  # UTF-8 BOM für Excel
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Seriennummer', 'Modell', 'Status', 'Eigentümer', 
        'Nennleistung (kVA)', 'Batteriekapazität (kWh)', 
        'Kaufdatum', 'Kaufpreis (€)', 'Standort'
    ])
    
    for device in queryset:
        writer.writerow([
            device.serial_number,
            device.get_model_display(),
            device.get_status_display(),
            str(device.owner),
            device.power_rating_kva,
            device.battery_capacity_kwh,
            device.purchase_date.strftime('%d.%m.%Y'),
            device.purchase_price,
            device.current_location or ''
        ])
    
    return response

export_devices_to_csv.short_description = "Ausgewählte Geräte als CSV exportieren"


def export_maintenance_to_csv(modeladmin, request, queryset):
    """Exportiert ausgewählte Wartungen als CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wartungen_export.csv"'
    response.write('\ufeff')
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Gerät', 'Wartungstyp', 'Geplant am', 'Durchgeführt am',
        'Abgeschlossen', 'Techniker', 'Kosten (€)'
    ])
    
    for maintenance in queryset:
        writer.writerow([
            str(maintenance.device),
            maintenance.get_maintenance_type_display(),
            maintenance.scheduled_date.strftime('%d.%m.%Y'),
            maintenance.completed_date.strftime('%d.%m.%Y') if maintenance.completed_date else '',
            'Ja' if maintenance.is_completed else 'Nein',
            maintenance.technician or '',
            maintenance.cost or ''
        ])
    
    return response

export_maintenance_to_csv.short_description = "Ausgewählte Wartungen als CSV exportieren"


class MaintenanceRecordInline(admin.TabularInline):
    """Inline-Anzeige der Wartungseinträge bei Geräten"""
    model = MaintenanceRecord
    extra = 0
    fields = ['maintenance_type', 'scheduled_date', 'completed_date', 'is_completed', 'cost']
    readonly_fields = ['created_at']


@admin.register(ButlerDevice)
class ButlerDeviceAdmin(admin.ModelAdmin):
    """Admin-Interface für Butler-Geräte"""
    
    list_display = [
        'serial_number', 
        'model', 
        'status', 
        'owner', 
        'power_rating_kva', 
        'battery_capacity_kwh',
        'created_at'
    ]
    
    list_filter = [
        'model', 
        'status', 
        'battery_technology', 
        'has_generator_start_control',
        'created_at'
    ]
    
    search_fields = [
        'serial_number', 
        'owner__username', 
        'owner__company_name',
        'current_location'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    actions = [export_devices_to_csv]
    
    fieldsets = (
        ('Basis-Informationen', {
            'fields': ('serial_number', 'model', 'status', 'owner')
        }),
        ('Technische Spezifikationen', {
            'fields': (
                'power_rating_kva', 
                'battery_capacity_kwh', 
                'battery_technology',
                'has_generator_start_control',
                'has_trailer'
            )
        }),
        ('Kaufdaten', {
            'fields': ('purchase_date', 'purchase_price', 'iab_amount', 'iab_year')
        }),
        ('Übergabe & Standort', {
            'fields': ('handover_to_rhk_date', 'current_location')
        }),
        ('Notizen', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadaten', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [MaintenanceRecordInline]


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    """Admin-Interface für Wartungseinträge"""
    
    list_display = [
        'device',
        'maintenance_type',
        'scheduled_date',
        'completed_date',
        'is_completed',
        'cost'
    ]
    
    list_filter = [
        'maintenance_type',
        'is_completed',
        'scheduled_date'
    ]
    
    search_fields = [
        'device__serial_number',
        'description',
        'technician'
    ]
    
    date_hierarchy = 'scheduled_date'
    actions = [export_maintenance_to_csv]
    
    fieldsets = (
        ('Wartungsinformationen', {
            'fields': ('device', 'maintenance_type', 'scheduled_date', 'completed_date')
        }),
        ('Details', {
            'fields': ('description', 'technician', 'cost', 'is_completed')
        }),
    )