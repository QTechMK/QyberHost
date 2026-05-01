from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import UserProfile


class QyberHostAccountAdapter(DefaultAccountAdapter):
    pass


class QyberHostSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        pending_role = request.session.pop("pending_social_role", None)

        profile, _ = UserProfile.objects.get_or_create(user=user)
        if pending_role in dict(UserProfile.PUBLIC_ROLE_CHOICES):
            profile.role = pending_role
        profile.is_sso_enabled = True
        profile.save()
        return user
