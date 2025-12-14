from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Erweitertes User-Model mit drei Benutzertypen:
    - IAB_INVESTOR: IAB-Endkunden, die Butler-Systeme besitzen
    - RHK_ADMIN: Mitarbeiter der rhk-mobil GmbH
    - COMMERCIAL_RENTER: Gewerbliche Mieter
    """
    
    class UserType(models.TextChoices):
        IAB_INVESTOR = 'IAB', 'IAB-Investor'
        RHK_ADMIN = 'RHK', 'rhk-mobil Admin'
        COMMERCIAL_RENTER = 'RENTER', 'Gewerblicher Mieter'
    
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.COMMERCIAL_RENTER,
        verbose_name="Benutzertyp"
    )
    
    # Firmendaten
    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Firmenname"
    )
    
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Steuernummer/USt-ID"
    )
    
    # Kontaktdaten
    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Telefon"
    )
    
    mobile = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Mobil"
    )
    
    # Adresse
    street = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Straße"
    )
    
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="PLZ"
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Stadt"
    )
    
    country = models.CharField(
        max_length=100,
        default="Deutschland",
        verbose_name="Land"
    )
    
    # Bankdaten (nur für IAB-Investoren für Ausschüttungen)
    iban = models.CharField(
        max_length=34,
        blank=True,
        null=True,
        verbose_name="IBAN"
    )
    
    bic = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="BIC"
    )
    
    bank_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Bankname"
    )
    
    # Steuerberater (für IAB-Investoren)
    tax_advisor_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Steuerberater Name"
    )
    
    tax_advisor_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Steuerberater E-Mail"
    )
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verifiziert"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notizen"
    )
    
    class Meta:
        verbose_name = "Benutzer"
        verbose_name_plural = "Benutzer"
        ordering = ['-created_at']
    
    def __str__(self):
        if self.company_name:
            return f"{self.get_full_name()} ({self.company_name})"
        return self.get_full_name() or self.username
    
    @property
    def is_iab_investor(self):
        """Prüft ob der User ein IAB-Investor ist"""
        return self.user_type == self.UserType.IAB_INVESTOR
    
    @property
    def is_rhk_admin(self):
        """Prüft ob der User ein rhk-mobil Admin ist"""
        return self.user_type == self.UserType.RHK_ADMIN
    
    @property
    def is_commercial_renter(self):
        """Prüft ob der User ein gewerblicher Mieter ist"""
        return self.user_type == self.UserType.COMMERCIAL_RENTER
