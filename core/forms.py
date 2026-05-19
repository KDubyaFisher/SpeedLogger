from django import forms

from .models import Customer, Site, SpeedTestResult

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

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            "customer",
            "name",
            "address",
            "city",
            "state",
            "zip_code",
            "notes",
        ]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

class SpeedTestResultForm(forms.ModelForm):
    class Meta:
        model = SpeedTestResult
        fields = [
            "site",
            "isp",
            "download_mbps",
            "upload_mbps",
            "ping_ms",
            "jitter_ms",
            "test_datetime",
            "notes",
        ]
        widgets = {
            "site": forms.Select(attrs={"class": "form-select"}),
            "isp": forms.TextInput(attrs={"class": "form-control"}),
            "download_mbps": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "upload_mbps": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "ping_ms": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "jitter_ms": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "test_datetime": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.test_datetime:
            self.initial["test_datetime"] = self.instance.test_datetime.strftime("%Y-%m-%dT%H:%M")