from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "contact_name",
            "contact_email",
            "phone",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "contact_name": forms.TextInput(attrs={"class": "form-control"}),
            "contact_email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }