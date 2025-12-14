from django.db import models
from django.conf import settings


class ButlerDevice(models.Model):
    """
    Butler-Energiesysteme mit verschiedenen Modellen
    """
    
    class DeviceModel(models.TextChoices):
        S_50_25 = 'S50/25', 'Butler S (50 kVA / 25 kWh)'
        M_150_150 = 'M150/150', 'Butler M (150 kVA / 150 kWh)'
    
    class DeviceStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Verfügbar'
        RENTED = 'RENTED', 'Vermietet'
        MAINTENANCE = 'MAINTENANCE', 'In Wartung'
        RESERVED = 'RESERVED', 'Reserviert'
        INACTIVE = 'INACTIVE', 'Inaktiv'
    
    class BatteryTechnology(models.TextChoices):
        LMO = 'LMO', 'Lithium Mangan Oxid (LMO)'
        NMC = 'NMC', 'Lithium Nickel Mangan Cobalt (NMC)'
    
    # Basis-Informationen
    serial_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Seriennummer"
    )
    
    model = models.CharField(
        max_length=20,
        choices=DeviceModel.choices,
        verbose_name="Modell"
    )
    
    status = models.CharField(
        max_length=20,
        choices=DeviceStatus.choices,
        default=DeviceStatus.AVAILABLE,
        verbose_name="Status"
    )
    
    # Eigentümer (IAB-Investor)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_devices',
        verbose_name="Eigentümer"
    )
    
    # Technische Spezifikationen
    power_rating_kva = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name="Nennleistung (kVA)"
    )
    
    battery_capacity_kwh = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name="Batteriekapazität (kWh)"
    )
    
    battery_technology = models.CharField(
        max_length=10,
        choices=BatteryTechnology.choices,
        default=BatteryTechnology.NMC,
        verbose_name="Batterietechnologie"
    )
    
    # Optionale Features
    has_generator_start_control = models.BooleanField(
        default=False,
        verbose_name="Generatorstart-Steuerung"
    )
    
    has_trailer = models.BooleanField(
        default=True,
        verbose_name="Mit Anhänger"
    )
    
    # Kaufdaten
    purchase_date = models.DateField(
        verbose_name="Kaufdatum"
    )
    
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Kaufpreis (€)"
    )
    
    # IAB-relevante Daten
    iab_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="IAB-Betrag (€)"
    )
    
    iab_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="IAB-Jahr"
    )
    
    # Übergabe an rhk-mobil
    handover_to_rhk_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Übergabe an rhk-mobil"
    )
    
    # Standort & GPS (für IoT später)
    current_location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Aktueller Standort"
    )
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notizen"
    )
    
    class Meta:
        verbose_name = "Butler-Gerät"
        verbose_name_plural = "Butler-Geräte"
        ordering = ['serial_number']
    
    def __str__(self):
        return f"{self.get_model_display()} - {self.serial_number}"
    
    @property
    def is_available(self):
        """Prüft ob das Gerät verfügbar ist"""
        return self.status == self.DeviceStatus.AVAILABLE
    
    @property
    def is_rented(self):
        """Prüft ob das Gerät vermietet ist"""
        return self.status == self.DeviceStatus.RENTED


class MaintenanceRecord(models.Model):
    """
    Wartungsprotokoll für Butler-Geräte
    """
    
    class MaintenanceType(models.TextChoices):
        ROUTINE = 'ROUTINE', 'Routinewartung'
        REPAIR = 'REPAIR', 'Reparatur'
        INSPECTION = 'INSPECTION', 'Inspektion'
        EMERGENCY = 'EMERGENCY', 'Notfall'
    
    device = models.ForeignKey(
        ButlerDevice,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        verbose_name="Gerät"
    )
    
    maintenance_type = models.CharField(
        max_length=20,
        choices=MaintenanceType.choices,
        verbose_name="Wartungstyp"
    )
    
    scheduled_date = models.DateField(
        verbose_name="Geplantes Datum"
    )
    
    completed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Durchgeführt am"
    )
    
    description = models.TextField(
        verbose_name="Beschreibung"
    )
    
    technician = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Techniker"
    )
    
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Kosten (€)"
    )
    
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Abgeschlossen"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Wartungseintrag"
        verbose_name_plural = "Wartungseinträge"
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.device.serial_number} - {self.get_maintenance_type_display()} ({self.scheduled_date})"
