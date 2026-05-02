from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from hostie.models import UserProfile

from .models import AccountMembership, CustomerAccount, CustomerDomain, CustomerService


ACTIVE_ACCOUNT_SESSION_KEY = "active_account_id"


DEMO_DOMAINS = [
    {
        "name": "hostie-demo.com",
        "registration_date": date(2025, 8, 22),
        "renewal_date": date(2026, 8, 21),
        "status": CustomerDomain.STATUS_ACTIVE,
        "ssl_status": CustomerDomain.SSL_INACTIVE,
    },
    {
        "name": "cloudpanel-demo.com.tr",
        "registration_date": date(2026, 2, 10),
        "renewal_date": date(2027, 2, 9),
        "status": CustomerDomain.STATUS_ACTIVE,
        "ssl_status": CustomerDomain.SSL_ACTIVE,
    },
    {
        "name": "vdsdemo.net",
        "registration_date": date(2024, 4, 2),
        "renewal_date": date(2026, 4, 2),
        "status": CustomerDomain.STATUS_REDEMPTION,
        "ssl_status": CustomerDomain.SSL_DOMAIN_INACTIVE,
    },
    {
        "name": "maildemo.com.tr",
        "registration_date": date(2024, 9, 27),
        "renewal_date": date(2026, 9, 26),
        "status": CustomerDomain.STATUS_ACTIVE,
        "ssl_status": CustomerDomain.SSL_ACTIVE,
    },
]


RENEWAL_PRICE_TABLE = {
    "com.tr": {"price": 125.82, "max_years": 4},
    "com": {"price": 651.67, "max_years": 4},
    "net": {"price": 589.90, "max_years": 4},
    "default": {"price": 399.90, "max_years": 3},
}

REDEMPTION_FEE = 99.00

DOMAIN_TLDS = [
    {"extension": ".com.tr", "register": 69.90, "transfer": 69.90, "renew": 125.82, "old_register": 104.85, "old_renew": 163.57, "spotlight": True, "sale": True},
    {"extension": ".tr", "register": 109.90, "transfer": 109.90, "renew": 197.82, "old_register": 164.85, "old_renew": 257.17, "spotlight": True, "sale": True},
    {"extension": ".net.tr", "register": 69.90, "transfer": 69.90, "renew": 125.82, "old_register": 104.85, "old_renew": 163.57, "spotlight": True, "sale": True},
    {"extension": ".com", "register": 521.52, "transfer": 521.52, "renew": 651.67, "old_register": 662.19, "old_renew": 706.02, "spotlight": True, "sale": True},
    {"extension": ".net", "register": 630.64, "transfer": 630.64, "renew": 893.59, "old_register": 766.50, "old_renew": 968.09, "spotlight": True, "sale": True},
    {"extension": ".org", "register": 437.81, "transfer": 550.44, "renew": 835.74, "old_register": 716.97, "old_renew": 905.42, "spotlight": True, "sale": True},
    {"extension": ".web.tr", "register": 69.90, "transfer": 69.90, "renew": 125.82, "old_register": 104.85, "old_renew": 163.57, "spotlight": True, "sale": True},
    {"extension": ".org.tr", "register": 69.90, "transfer": 69.90, "renew": 125.82, "old_register": 104.85, "old_renew": 163.57, "spotlight": False, "sale": True},
    {"extension": ".gen.tr", "register": 69.90, "transfer": 69.90, "renew": 125.82, "old_register": 104.85, "old_renew": 163.57, "spotlight": False, "sale": True},
    {"extension": ".biz", "register": 925.14, "transfer": 925.14, "renew": 1230.16, "old_register": 1051.36, "old_renew": 1332.71, "spotlight": False, "sale": True},
    {"extension": ".co", "register": 1489.17, "transfer": 1489.17, "renew": 1966.42, "old_register": 1692.08, "old_renew": 2130.32, "spotlight": False, "sale": True},
    {"extension": ".cloud", "register": 963.71, "transfer": 963.71, "renew": 1577.25, "old_register": 1095.18, "old_renew": 1708.73, "spotlight": False, "sale": True},
    {"extension": ".info", "register": 1252.95, "transfer": 1359.01, "renew": 1650.88, "old_register": 1423.87, "old_renew": 1788.49, "spotlight": False, "sale": True},
    {"extension": ".io", "register": 2530.44, "transfer": 2530.44, "renew": 3286.42, "old_register": 2875.35, "old_renew": 3560.33, "spotlight": False, "sale": False},
    {"extension": ".app", "register": 886.58, "transfer": 886.58, "renew": 1182.83, "old_register": 1007.53, "old_renew": 1281.44, "spotlight": False, "sale": False},
    {"extension": ".ai", "register": 7800.81, "transfer": 7800.81, "renew": 7800.81, "old_register": 7456.00, "old_renew": 7456.00, "spotlight": False, "sale": False},
    {"extension": ".xyz", "register": 131.04, "transfer": 741.95, "renew": 1004.03, "old_register": 843.19, "old_renew": 1087.73, "spotlight": False, "sale": True},
    {"extension": ".site", "register": 1686.82, "transfer": 1686.82, "renew": 1840.20, "old_register": 1916.90, "old_renew": 1993.59, "spotlight": False, "sale": False},
    {"extension": ".online", "register": 1619.33, "transfer": 1619.33, "renew": 1766.58, "old_register": 1840.20, "old_renew": 1913.83, "spotlight": False, "sale": False},
    {"extension": ".shop", "register": 1894.11, "transfer": 1894.11, "renew": 2492.32, "old_register": 2152.24, "old_renew": 2700.05, "spotlight": False, "sale": False},
]


def account_type_for_user(user):
    profile = getattr(user, "profile", None)
    if profile is None:
        return CustomerAccount.TYPE_INDIVIDUAL

    if profile.role == UserProfile.ROLE_COMPANY:
        return CustomerAccount.TYPE_COMPANY
    if profile.role == UserProfile.ROLE_AFFILIATE:
        return CustomerAccount.TYPE_AFFILIATE
    return CustomerAccount.TYPE_INDIVIDUAL


def default_account_name(user):
    profile = getattr(user, "profile", None)
    if profile and profile.company_name:
        return profile.company_name

    full_name = user.get_full_name().strip()
    return full_name or user.email or user.username


def ensure_default_account(user):
    membership = (
        AccountMembership.objects
        .select_related("account")
        .filter(user=user, is_active=True, account__is_active=True)
        .first()
    )
    if membership:
        return membership

    account = CustomerAccount.objects.create(
        name=default_account_name(user),
        account_type=account_type_for_user(user),
        email=user.email,
        phone=getattr(getattr(user, "profile", None), "phone", ""),
    )
    return AccountMembership.objects.create(
        user=user,
        account=account,
        role=AccountMembership.ROLE_OWNER,
    )


def ensure_demo_domains(account):
    if account.domains.exists():
        return

    for domain_data in DEMO_DOMAINS:
        CustomerDomain.objects.get_or_create(
            account=account,
            name=domain_data["name"],
            defaults={
                "registration_date": domain_data["registration_date"],
                "renewal_date": domain_data["renewal_date"],
                "status": domain_data["status"],
                "ssl_status": domain_data["ssl_status"],
                "auto_renew": True,
                "registrar": "Demo Registrar",
            },
        )


def get_domain_extension(domain_name):
    parts = domain_name.lower().split(".")
    if len(parts) >= 3 and parts[-2] == "com" and parts[-1] == "tr":
        return "com.tr"
    return parts[-1] if parts else "default"


def format_try(amount):
    return f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + "TL"


def enrich_tlds_for_template(tlds):
    enriched = []
    for tld in tlds:
        item = tld.copy()
        item["register_display"] = format_try(item["register"])
        item["transfer_display"] = format_try(item["transfer"])
        item["renew_display"] = format_try(item["renew"])
        item["old_register_display"] = format_try(item["old_register"])
        item["old_renew_display"] = format_try(item["old_renew"])
        enriched.append(item)
    return enriched


def build_renewal_options(domain):
    extension = get_domain_extension(domain.name)
    pricing = RENEWAL_PRICE_TABLE.get(extension, RENEWAL_PRICE_TABLE["default"])
    max_years = 1 if domain.status == CustomerDomain.STATUS_REDEMPTION else pricing["max_years"]
    options = []

    for year in range(1, max_years + 1):
        base_price = pricing["price"] * year
        recovery_fee = REDEMPTION_FEE if domain.status == CustomerDomain.STATUS_REDEMPTION else 0
        total = base_price + recovery_fee
        options.append({
            "years": year,
            "base_price": base_price,
            "recovery_fee": recovery_fee,
            "total": total,
            "label": f"{year} Yil - {format_try(base_price)}",
            "recovery_label": f" + {format_try(recovery_fee)} Domain Kurtarma" if recovery_fee else "",
        })

    return options


def relative_month_label(days):
    if days == 0:
        return "bugun"

    abs_days = abs(days)
    if abs_days < 31:
        unit = "gun"
        value = abs_days
    elif abs_days < 365:
        unit = "ay"
        value = max(1, round(abs_days / 30))
    else:
        unit = "yil"
        value = max(1, round(abs_days / 365))

    return f"{value} {unit} {'sonra' if days > 0 else 'once'}"


def build_domain_renewal_items(domains_qs):
    today = timezone.localdate()
    items = []

    for domain in domains_qs:
        days_remaining = (domain.renewal_date - today).days
        is_renewable = days_remaining >= -90
        badge_class = "success"
        if days_remaining < 0:
            badge_class = "danger" if is_renewable else "info"
            status_label = (
                f"{abs(days_remaining)} gun once suresi doldu"
                if is_renewable
                else "Yenilenme Zamani Gecmistir"
            )
        else:
            status_label = f"{days_remaining} gun sonra doluyor"

        items.append({
            "domain": domain,
            "days_remaining": days_remaining,
            "status_label": status_label,
            "badge_class": badge_class,
            "relative_label": relative_month_label(days_remaining),
            "is_renewable": is_renewable,
            "options": build_renewal_options(domain) if is_renewable else [],
        })

    return items


def get_user_memberships(user):
    ensure_default_account(user)
    return (
        AccountMembership.objects
        .select_related("account")
        .filter(user=user, is_active=True, account__is_active=True)
        .order_by("account__name")
    )


def set_active_membership(request, membership):
    request.session[ACTIVE_ACCOUNT_SESSION_KEY] = str(membership.account_id)
    request.session["active_membership_role"] = membership.role


def get_active_membership(request):
    account_id = request.session.get(ACTIVE_ACCOUNT_SESSION_KEY)
    if not account_id:
        return None

    try:
        return AccountMembership.objects.select_related("account").get(
            user=request.user,
            account_id=account_id,
            is_active=True,
            account__is_active=True,
        )
    except (AccountMembership.DoesNotExist, ValueError):
        request.session.pop(ACTIVE_ACCOUNT_SESSION_KEY, None)
        request.session.pop("active_membership_role", None)
        return None


@login_required
def entry(request):
    memberships = list(get_user_memberships(request.user))

    if len(memberships) == 1:
        set_active_membership(request, memberships[0])
        return redirect("nexadash:index")

    return redirect("nexadash:account-select")


@login_required
def account_select(request):
    memberships = get_user_memberships(request.user)
    context = {
        "page_title": "Hesap Sec",
        "memberships": memberships,
    }
    return render(request, "nexadash/customer/account-select.html", context)


@login_required
def account_switch(request, account_id):
    if request.method != "POST":
        raise Http404()

    membership = get_object_or_404(
        AccountMembership.objects.select_related("account"),
        user=request.user,
        account_id=account_id,
        is_active=True,
        account__is_active=True,
    )
    set_active_membership(request, membership)
    return redirect("nexadash:index")


@login_required
def domains(request):
    membership = get_active_membership(request)
    if membership is None:
        return redirect("nexadash:entry")

    request.active_membership = membership
    request.active_account = membership.account
    ensure_demo_domains(membership.account)

    today = timezone.localdate()
    expiring_limit = today + timedelta(days=30)
    all_domains = membership.account.domains.all()
    active_filter = request.GET.get("status", "")

    domains_qs = all_domains
    if active_filter == CustomerDomain.STATUS_ACTIVE:
        domains_qs = domains_qs.filter(status=CustomerDomain.STATUS_ACTIVE)
    elif active_filter == CustomerDomain.STATUS_REDEMPTION:
        domains_qs = domains_qs.filter(status=CustomerDomain.STATUS_REDEMPTION)
    elif active_filter == "expiring":
        domains_qs = domains_qs.filter(renewal_date__lte=expiring_limit)

    stats = {
        "total": all_domains.count(),
        "active": all_domains.filter(status=CustomerDomain.STATUS_ACTIVE).count(),
        "redemption": all_domains.filter(status=CustomerDomain.STATUS_REDEMPTION).count(),
        "expiring": all_domains.filter(renewal_date__lte=expiring_limit).count(),
    }
    context = {
        "page_title": "Domainlerimi Listele",
        "active_account": membership.account,
        "active_membership": membership,
        "domains": domains_qs,
        "stats": stats,
        "active_filter": active_filter,
        "can_manage_technical": membership.can_manage_technical,
        "can_manage_billing": membership.can_manage_billing,
    }
    return render(request, "nexadash/customer/domains.html", context)


@login_required
def domain_renewals(request):
    membership = get_active_membership(request)
    if membership is None:
        return redirect("nexadash:entry")

    request.active_membership = membership
    request.active_account = membership.account
    ensure_demo_domains(membership.account)

    domains_qs = membership.account.domains.exclude(status=CustomerDomain.STATUS_PENDING)
    renewal_items = build_domain_renewal_items(domains_qs)
    context = {
        "page_title": "Domain Yenilemeleri",
        "active_account": membership.account,
        "active_membership": membership,
        "renewal_items": renewal_items,
        "can_manage_billing": membership.can_manage_billing,
    }
    return render(request, "nexadash/customer/domain-renewals.html", context)


@login_required
def domain_register(request):
    membership = get_active_membership(request)
    if membership is None:
        return redirect("nexadash:entry")

    request.active_membership = membership
    request.active_account = membership.account
    tlds = enrich_tlds_for_template(DOMAIN_TLDS)
    context = {
        "page_title": "Domain Kaydet",
        "active_account": membership.account,
        "active_membership": membership,
        "tlds": tlds,
        "spotlight_tlds": [tld for tld in tlds if tld["spotlight"]],
        "can_manage_billing": membership.can_manage_billing,
    }
    return render(request, "nexadash/customer/domain-register.html", context)


@login_required
def domain_checker(request):
    membership = get_active_membership(request)
    if membership is None:
        return redirect("nexadash:entry")

    request.active_membership = membership
    request.active_account = membership.account
    ensure_demo_domains(membership.account)

    tlds = enrich_tlds_for_template(DOMAIN_TLDS)
    domains = membership.account.domains.all()
    context = {
        "page_title": "Domain Sorgula",
        "active_account": membership.account,
        "active_membership": membership,
        "tlds": tlds,
        "spotlight_tlds": [tld for tld in tlds if tld["spotlight"]],
        "owned_domains": [domain.name.lower() for domain in domains],
        "can_manage_billing": membership.can_manage_billing,
    }
    return render(request, "nexadash/customer/domain-checker.html", context)


@login_required
def whois_lookup(request):
    membership = get_active_membership(request)
    if membership is None:
        return redirect("nexadash:entry")

    request.active_membership = membership
    request.active_account = membership.account
    ensure_demo_domains(membership.account)

    domains = membership.account.domains.all()
    context = {
        "page_title": "WHOIS Sorgula",
        "active_account": membership.account,
        "active_membership": membership,
        "owned_domains": [domain.name.lower() for domain in domains],
    }
    return render(request, "nexadash/customer/whois.html", context)


@login_required
def domain_transfer(request):
    membership = get_active_membership(request)
    if membership is None:
        return redirect("nexadash:entry")

    request.active_membership = membership
    request.active_account = membership.account
    ensure_demo_domains(membership.account)

    tlds = enrich_tlds_for_template(DOMAIN_TLDS)
    domains = membership.account.domains.all()
    context = {
        "page_title": "Domain Transferi",
        "active_account": membership.account,
        "active_membership": membership,
        "tlds": tlds,
        "popular_transfer_tlds": [tld for tld in tlds if tld["spotlight"]],
        "owned_domains": [domain.name.lower() for domain in domains],
        "can_manage_billing": membership.can_manage_billing,
    }
    return render(request, "nexadash/customer/domain-transfer.html", context)


@login_required
def services(request):
    membership = get_active_membership(request)
    if membership is None:
        return redirect("nexadash:entry")

    request.active_membership = membership
    request.active_account = membership.account

    status_map = {
        "active": "Aktif",
        "pending": "Beklemede",
        "suspended": "Durduruldu",
    }
    badge_map = {
        "active": "success",
        "pending": "warning",
        "suspended": "danger",
    }

    services_qs = membership.account.services.all()
    services_list = []
    for service in services_qs:
        item = {
            "id": service.id,
            "name": service.name,
            "domain": service.domain,
            "price": float(service.price),
            "period": service.period,
            "renewal_date": service.renewal_date,
            "status": service.status,
        }
        item["status_label"] = status_map.get(item["status"], item["status"])
        item["badge_class"] = badge_map.get(item["status"], "info")
        item["price_display"] = format_try(item["price"])
        services_list.append(item)

    stats = {
        "total": len(services_list),
        "active": len([s for s in services_list if s["status"] == "active"]),
        "pending": len([s for s in services_list if s["status"] == "pending"]),
        "suspended": len([s for s in services_list if s["status"] == "suspended"]),
    }

    context = {
        "page_title": "Hizmetlerim",
        "active_account": membership.account,
        "active_membership": membership,
        "services": services_list,
        "stats": stats,
        "can_manage_billing": membership.can_manage_billing,
    }
    return render(request, "nexadash/customer/services.html", context)


def require_active_membership(view_func):
    @login_required
    def wrapped(request, *args, **kwargs):
        membership = get_active_membership(request)
        if membership is None:
            return redirect("nexadash:entry")

        request.active_membership = membership
        request.active_account = membership.account
        return view_func(request, *args, **kwargs)

    return wrapped


def require_account_permission(permission_name):
    def decorator(view_func):
        @require_active_membership
        def wrapped(request, *args, **kwargs):
            membership = request.active_membership
            permission_map = {
                "billing": membership.can_manage_billing,
                "technical": membership.can_manage_technical,
                "users": membership.can_manage_users,
                "affiliate": membership.can_manage_affiliate,
                "tickets": membership.can_open_tickets,
            }
            if not permission_map.get(permission_name, False):
                return HttpResponseForbidden("Bu hesapta bu islem icin yetkiniz yok.")
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
