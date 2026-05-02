from .models import CustomerService


ACTIVE_ACCOUNT_SESSION_KEY = "active_account_id"


def customer_service_nav(request):
    default = {
        "has_any": False,
        "has_hosting": False,
        "has_vps": False,
        "has_ssl": False,
        "has_email": False,
    }

    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {"service_nav": default}

    account_id = request.session.get(ACTIVE_ACCOUNT_SESSION_KEY)
    if not account_id:
        return {"service_nav": default}

    service_types = set(
        CustomerService.objects.filter(account_id=account_id)
        .values_list("service_type", flat=True)
    )
    service_nav = {
        "has_any": bool(service_types),
        "has_hosting": CustomerService.TYPE_HOSTING in service_types,
        "has_vps": CustomerService.TYPE_VPS in service_types,
        "has_ssl": CustomerService.TYPE_SSL in service_types,
        "has_email": CustomerService.TYPE_EMAIL in service_types,
    }
    return {"service_nav": service_nav}
