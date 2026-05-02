import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class CustomerAccount(models.Model):
    TYPE_INDIVIDUAL = "individual"
    TYPE_COMPANY = "company"
    TYPE_AFFILIATE = "affiliate"

    ACCOUNT_TYPE_CHOICES = [
        (TYPE_INDIVIDUAL, "Bireysel Hesap"),
        (TYPE_COMPANY, "Sirket Hesabi"),
        (TYPE_AFFILIATE, "Affiliate Hesabi"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    account_type = models.CharField(
        max_length=24,
        choices=ACCOUNT_TYPE_CHOICES,
        default=TYPE_INDIVIDUAL,
    )
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    tax_number = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AccountMembership(models.Model):
    ROLE_OWNER = "owner"
    ROLE_ADMIN = "admin"
    ROLE_TECHNICAL = "technical"
    ROLE_BILLING = "billing"
    ROLE_SUPPORT_VIEWER = "support_viewer"
    ROLE_AFFILIATE_MANAGER = "affiliate_manager"

    ROLE_CHOICES = [
        (ROLE_OWNER, "Hesap Sahibi"),
        (ROLE_ADMIN, "Yonetici"),
        (ROLE_TECHNICAL, "Teknik Sorumlu"),
        (ROLE_BILLING, "Muhasebe Yetkilisi"),
        (ROLE_SUPPORT_VIEWER, "Destek Goruntuleyici"),
        (ROLE_AFFILIATE_MANAGER, "Affiliate Yetkilisi"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="account_memberships",
    )
    account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=32, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "account")
        ordering = ["account__name", "role"]

    def __str__(self):
        return f"{self.user} - {self.account} ({self.get_role_display()})"

    @property
    def can_manage_billing(self):
        return self.role in {self.ROLE_OWNER, self.ROLE_ADMIN, self.ROLE_BILLING}

    @property
    def can_manage_technical(self):
        return self.role in {self.ROLE_OWNER, self.ROLE_ADMIN, self.ROLE_TECHNICAL}

    @property
    def can_manage_users(self):
        return self.role in {self.ROLE_OWNER, self.ROLE_ADMIN}

    @property
    def can_manage_affiliate(self):
        return self.role in {self.ROLE_OWNER, self.ROLE_ADMIN, self.ROLE_AFFILIATE_MANAGER}

    @property
    def can_open_tickets(self):
        return self.role in {
            self.ROLE_OWNER,
            self.ROLE_ADMIN,
            self.ROLE_TECHNICAL,
            self.ROLE_BILLING,
        }


class CustomerDomain(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_REDEMPTION = "redemption"
    STATUS_EXPIRED = "expired"
    STATUS_PENDING = "pending"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Aktif"),
        (STATUS_REDEMPTION, "Kurtarma Donemi"),
        (STATUS_EXPIRED, "Suresi Doldu"),
        (STATUS_PENDING, "Beklemede"),
    ]

    SSL_ACTIVE = "active"
    SSL_INACTIVE = "inactive"
    SSL_DOMAIN_INACTIVE = "domain_inactive"

    SSL_CHOICES = [
        (SSL_ACTIVE, "Gecerli SSL Sertifikasi"),
        (SSL_INACTIVE, "SSL Sertifikasi Tespit Edilemedi"),
        (SSL_DOMAIN_INACTIVE, "Domain Aktif Degil"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name="domains",
    )
    name = models.CharField(max_length=255)
    registration_date = models.DateField()
    renewal_date = models.DateField()
    auto_renew = models.BooleanField(default=True)
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    ssl_status = models.CharField(max_length=24, choices=SSL_CHOICES, default=SSL_INACTIVE)
    registrar = models.CharField(max_length=120, blank=True)
    is_locked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("account", "name")
        ordering = ["renewal_date", "name"]

    def __str__(self):
        return self.name

    @property
    def is_expiring_soon(self):
        return self.renewal_date <= timezone.localdate() + timedelta(days=30)


class CustomerService(models.Model):
    TYPE_HOSTING = "hosting"
    TYPE_VPS = "vps_vds"
    TYPE_SSL = "ssl"
    TYPE_EMAIL = "email"

    SERVICE_TYPE_CHOICES = [
        (TYPE_HOSTING, "Hosting"),
        (TYPE_VPS, "VPS / VDS"),
        (TYPE_SSL, "SSL Sertifikasi"),
        (TYPE_EMAIL, "E-Mail Hizmeti"),
    ]

    STATUS_ACTIVE = "active"
    STATUS_PENDING = "pending"
    STATUS_SUSPENDED = "suspended"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Aktif"),
        (STATUS_PENDING, "Beklemede"),
        (STATUS_SUSPENDED, "Durduruldu"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name="services",
    )
    service_type = models.CharField(max_length=16, choices=SERVICE_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    period = models.CharField(max_length=64, default="12 Ay")
    renewal_date = models.DateField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["renewal_date", "name"]

    def __str__(self):
        return self.name
