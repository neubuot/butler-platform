from django.contrib import admin
from .models import ButlerDevice, MaintenanceRecord


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
    
    fieldsets = (
        ('Wartungsinformationen', {
            'fields': ('device', 'maintenance_type', 'scheduled_date', 'completed_date')
        }),
        ('Details', {
            'fields': ('description', 'technician', 'cost', 'is_completed')
        }),
    )
