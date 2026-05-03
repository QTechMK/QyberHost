from allauth.account.adapter import DefaultAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User

from .models import UserProfile


class QyberHostAccountAdapter(DefaultAccountAdapter):
    pass


class QyberHostSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        account = sociallogin.account
        provider = account.provider
        email = (sociallogin.user.email or "").strip().lower()

        if provider != "google":
            return

        if not email:
            messages.error(request, "Google hesabi e-posta bilgisi donmedi. Lutfen farkli bir hesap deneyin.")
            raise ImmediateHttpResponse(redirect("sign-in"))

        # Logged-in users are connecting Google on account settings page.
        if request.user.is_authenticated:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            locked_email = (profile.sso_email or "").strip().lower()

            if locked_email and locked_email != email:
                messages.error(
                    request,
                    "Bu hesap yalnizca eslestirilmis Google e-postasi ile baglanabilir.",
                )
                raise ImmediateHttpResponse(redirect("nexadash:account-login-security"))
            return

        existing_user = User.objects.filter(email__iexact=email).first()
        if not existing_user:
            return

        profile, _ = UserProfile.objects.get_or_create(user=existing_user)
        locked_email = (profile.sso_email or "").strip().lower()
        if profile.is_sso_enabled and locked_email and locked_email != email:
            messages.error(
                request,
                "Bu hesap icin SSO yalnizca eslestirilmis Google e-postasi ile kullanilabilir.",
            )
            raise ImmediateHttpResponse(redirect("sign-in"))

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        pending_role = request.session.pop("pending_social_role", None)
        provider = sociallogin.account.provider
        email = (sociallogin.user.email or user.email or "").strip().lower()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        if pending_role in dict(UserProfile.PUBLIC_ROLE_CHOICES):
            profile.role = pending_role
        if provider == "google":
            profile.is_sso_enabled = True
            profile.sso_provider = "google"
            if email:
                profile.sso_email = email
        profile.save()
        return user
