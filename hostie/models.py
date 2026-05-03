# contact/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class UserProfile(models.Model):
    ROLE_INDIVIDUAL = "individual_customer"
    ROLE_COMPANY = "company_customer"
    ROLE_AFFILIATE = "affiliate_partner"
    ROLE_SUPPORT = "support_operator"
    ROLE_ADMIN = "super_admin"

    ROLE_CHOICES = [
        (ROLE_INDIVIDUAL, "Bireysel Musteri"),
        (ROLE_COMPANY, "Kurumsal Musteri"),
        (ROLE_AFFILIATE, "Affiliate / Is Ortagi"),
        (ROLE_SUPPORT, "Destek / Operasyon"),
        (ROLE_ADMIN, "Yonetici / Super Admin"),
    ]

    PUBLIC_ROLE_CHOICES = [
        (ROLE_INDIVIDUAL, "Bireysel Musteri"),
        (ROLE_COMPANY, "Sirket / Kurumsal Musteri"),
        (ROLE_AFFILIATE, "Affiliate / Is Ortagi"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=ROLE_INDIVIDUAL)
    company_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_sso_enabled = models.BooleanField(default=False)
    sso_provider = models.CharField(max_length=32, blank=True)
    sso_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        return

    UserProfile.objects.get_or_create(user=instance)
