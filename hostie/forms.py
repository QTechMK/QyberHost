# contact/forms.py
from django import forms

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
        required=True
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    consent = forms.BooleanField(required=True)
