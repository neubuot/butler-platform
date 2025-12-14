from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from assets.models import ButlerDevice


class Booking(models.Model):
    """
    Buchungen für Butler-Geräte durch gewerbliche Mieter
    """
    
    class BookingStatus(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Angefragt'
        CONFIRMED = 'CONFIRMED', 'Bestätigt'
        REJECTED = 'REJECTED', 'Abgelehnt'
        ACTIVE = 'ACTIVE', 'Aktiv (läuft)'
        COMPLETED = 'COMPLETED', 'Abgeschlossen'
        CANCELLED = 'CANCELLED', 'Storniert'
    
    class UsageType(models.TextChoices):
        CONSTRUCTION = 'CONSTRUCTION', 'Baustelle/Kranbetrieb'
        FILM = 'FILM', 'Film-/Videoproduktion'
        EVENT = 'EVENT', 'Event/Veranstaltung'
        EMERGENCY = 'EMERGENCY', 'Katastrophenschutz'
        OTHER = 'OTHER', 'Sonstiges'
    
    # Buchungsreferenz
    booking_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Buchungsnummer"
    )
    
    # Gerät und Mieter
    device = models.ForeignKey(
        ButlerDevice,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name="Butler-Gerät"
    )
    
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='rentals',
        verbose_name="Mieter"
    )
    
    # Zeitraum
    start_date = models.DateField(
        verbose_name="Startdatum"
    )
    
    end_date = models.DateField(
        verbose_name="Enddatum"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.REQUESTED,
        verbose_name="Status"
    )
    
    # Einsatzbereich
    usage_type = models.CharField(
        max_length=20,
        choices=UsageType.choices,
        verbose_name="Einsatzbereich"
    )
    
    usage_description = models.TextField(
        verbose_name="Einsatzbeschreibung"
    )
    
    # Standort während der Miete
    delivery_address = models.TextField(
        verbose_name="Lieferadresse"
    )
    
    # Kostenberechnung
    daily_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Tagessatz (€)"
    )
    
    handling_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Handling-Gebühr (€)"
    )
    
    transport_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Transportkosten (€)"
    )
    
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Gesamtpreis (€)"
    )
    
    # Genehmigung
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_bookings',
        verbose_name="Genehmigt von"
    )
    
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Genehmigt am"
    )
    
    rejection_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ablehnungsgrund"
    )
    
    # Kontaktperson beim Mieter
    contact_person = models.CharField(
        max_length=200,
        verbose_name="Kontaktperson"
    )
    
    contact_phone = models.CharField(
        max_length=30,
        verbose_name="Telefon"
    )
    
    contact_email = models.EmailField(
        verbose_name="E-Mail"
    )
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Interne Notizen"
    )
    
    class Meta:
        verbose_name = "Buchung"
        verbose_name_plural = "Buchungen"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.booking_number} - {self.device.serial_number} ({self.start_date} bis {self.end_date})"
    
    def clean(self):
        """Validierung"""
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError("Enddatum muss nach Startdatum liegen")
            
            # Prüfe ob Gerät in diesem Zeitraum bereits gebucht ist
            overlapping = Booking.objects.filter(
                device=self.device,
                status__in=[self.BookingStatus.CONFIRMED, self.BookingStatus.ACTIVE]
            ).exclude(pk=self.pk).filter(
                start_date__lt=self.end_date,
                end_date__gt=self.start_date
            )
            
            if overlapping.exists():
                raise ValidationError(
                    f"Gerät ist im Zeitraum {self.start_date} bis {self.end_date} bereits gebucht"
                )
    
    def save(self, *args, **kwargs):
        # Generiere Buchungsnummer wenn noch keine vorhanden
        if not self.booking_number:
            # Format: BK-YYYYMMDD-XXXX
            today = timezone.now()
            prefix = f"BK-{today.strftime('%Y%m%d')}"
            last_booking = Booking.objects.filter(
                booking_number__startswith=prefix
            ).order_by('-booking_number').first()
            
            if last_booking:
                last_num = int(last_booking.booking_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.booking_number = f"{prefix}-{new_num:04d}"
        
        super().save(*args, **kwargs)
    
    @property
    def duration_days(self):
        """Berechnet die Dauer der Buchung in Tagen"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0
    
    @property
    def is_active(self):
        """Prüft ob die Buchung aktuell aktiv ist"""
        today = timezone.now().date()
        return (
            self.status == self.BookingStatus.ACTIVE and
            self.start_date <= today <= self.end_date
        )
