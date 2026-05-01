from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    country = forms.ChoiceField(
        choices=[
            ("Bangladesh", "Bangladesh"),
            ("India", "India"),
            ("Pakistan", "Pakistan"),
            ("Nepal", "Nepal"),
            ("Maldives", "Maldives"),
        ],
        required=True,
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    consent = forms.BooleanField(required=True)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=UserProfile.PUBLIC_ROLE_CHOICES)
    company_name = forms.CharField(max_length=255, required=False)
    phone = forms.CharField(max_length=30, required=False)
    privacy_agree = forms.BooleanField(required=True)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanici adi zaten kullaniliyor.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kayitli.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        role = cleaned_data.get("role")
        company_name = cleaned_data.get("company_name", "").strip()

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Sifreler eslesmiyor.")

        if role == UserProfile.ROLE_COMPANY and not company_name:
            self.add_error("company_name", "Kurumsal hesap icin sirket adi gerekli.")

        return cleaned_data


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False)
