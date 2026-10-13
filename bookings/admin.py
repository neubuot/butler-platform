from django.contrib import admin
from django.utils.html import format_html
from .models import Booking
import csv
from django.http import HttpResponse


def export_bookings_to_csv(modeladmin, request, queryset):
    """Exportiert ausgewählte Buchungen als CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="buchungen_export.csv"'
    response.write('\ufeff')  # UTF-8 BOM für Excel
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Buchungsnummer', 'Gerät', 'Mieter', 'Startdatum', 'Enddatum',
        'Dauer (Tage)', 'Status', 'Einsatzbereich', 'Gesamtpreis (€)',
        'Kontaktperson', 'Telefon', 'Erstellt am'
    ])
    
    for booking in queryset:
        writer.writerow([
            booking.booking_number,
            booking.device.serial_number,
            str(booking.renter),
            booking.start_date.strftime('%d.%m.%Y'),
            booking.end_date.strftime('%d.%m.%Y'),
            booking.duration_days,
            booking.get_status_display(),
            booking.get_usage_type_display(),
            booking.total_price,
            booking.contact_person,
            booking.contact_phone,
            booking.created_at.strftime('%d.%m.%Y %H:%M')
        ])
    
    return response

export_bookings_to_csv.short_description = "Ausgewählte Buchungen als CSV exportieren"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin-Interface für Buchungen"""
    
    list_display = [
        'booking_number',
        'device',
        'renter',
        'start_date',
        'end_date',
        'status_badge',
        'usage_type',
        'total_price',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'usage_type',
        'start_date',
        'created_at'
    ]
    
    search_fields = [
        'booking_number',
        'device__serial_number',
        'renter__username',
        'renter__company_name',
        'contact_person'
    ]
    
    readonly_fields = [
        'booking_number',
        'created_at',
        'updated_at',
        'duration_days'
    ]
    
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Buchungsdetails', {
            'fields': (
                'booking_number',
                'device',
                'renter',
                'status'
            )
        }),
        ('Zeitraum', {
            'fields': (
                'start_date',
                'end_date',
                'duration_days'
            )
        }),
        ('Einsatzdetails', {
            'fields': (
                'usage_type',
                'usage_description',
                'delivery_address'
            )
        }),
        ('Kostenberechnung', {
            'fields': (
                'daily_rate',
                'handling_fee',
                'transport_fee',
                'total_price'
            )
        }),
        ('Kontakt', {
            'fields': (
                'contact_person',
                'contact_phone',
                'contact_email'
            )
        }),
        ('Genehmigung', {
            'fields': (
                'approved_by',
                'approved_at',
                'rejection_reason'
            ),
            'classes': ('collapse',)
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
    
    def status_badge(self, obj):
        """Zeigt Status als farbige Badge"""
        colors = {
            'REQUESTED': '#FFA500',  # Orange
            'CONFIRMED': '#4CAF50',  # Grün
            'REJECTED': '#F44336',   # Rot
            'ACTIVE': '#2196F3',     # Blau
            'COMPLETED': '#9E9E9E',  # Grau
            'CANCELLED': '#757575',  # Dunkelgrau
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def duration_days(self, obj):
        """Zeigt die Dauer in Tagen"""
        return f"{obj.duration_days} Tage"
    duration_days.short_description = 'Dauer'
    
    actions = ['approve_bookings', 'reject_bookings', 'mark_as_completed', export_bookings_to_csv]
    
    def approve_bookings(self, request, queryset):
        """Aktion zum Genehmigen von Buchungen"""
        from django.utils import timezone
        updated = queryset.filter(status='REQUESTED').update(
            status='CONFIRMED',
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f"{updated} Buchung(en) wurden genehmigt.")
    approve_bookings.short_description = "Ausgewählte Buchungen genehmigen"
    
    def reject_bookings(self, request, queryset):
        """Aktion zum Ablehnen von Buchungen"""
        updated = queryset.filter(status='REQUESTED').update(status='REJECTED')
        self.message_user(request, f"{updated} Buchung(en) wurden abgelehnt.")
    reject_bookings.short_description = "Ausgewählte Buchungen ablehnen"
    
    def mark_as_completed(self, request, queryset):
        """Aktion zum Markieren als abgeschlossen"""
        updated = queryset.filter(status__in=['CONFIRMED', 'ACTIVE']).update(status='COMPLETED')
        self.message_user(request, f"{updated} Buchung(en) wurden als abgeschlossen markiert.")
    mark_as_completed.short_description = "Als abgeschlossen markieren"