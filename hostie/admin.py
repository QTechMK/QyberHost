from django.contrib import admin

from .models import ContactMessage, UserProfile


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "country", "created_at")
    search_fields = ("name", "email", "phone")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "company_name", "phone", "is_sso_enabled", "updated_at")
    list_filter = ("role", "is_sso_enabled")
    search_fields = ("user__username", "user__email", "company_name", "phone")
