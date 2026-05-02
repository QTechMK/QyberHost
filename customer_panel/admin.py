from django.contrib import admin

from .models import AccountMembership, CustomerAccount, CustomerDomain


class AccountMembershipInline(admin.TabularInline):
    model = AccountMembership
    extra = 0


@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "email", "is_active", "created_at")
    list_filter = ("account_type", "is_active")
    search_fields = ("name", "email", "tax_number")
    inlines = [AccountMembershipInline]


@admin.register(AccountMembership)
class AccountMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "account", "role", "is_active", "created_at")
    list_filter = ("role", "is_active")
    search_fields = ("user__username", "user__email", "account__name")


@admin.register(CustomerDomain)
class CustomerDomainAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "account",
        "status",
        "ssl_status",
        "auto_renew",
        "renewal_date",
        "registrar",
    )
    list_filter = ("status", "ssl_status", "auto_renew", "registrar")
    search_fields = ("name", "account__name", "registrar")
    date_hierarchy = "renewal_date"
