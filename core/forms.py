from django import forms
from django.core.exceptions import ValidationError

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

        def clean_name(self):
            name = self.cleaned_data["name"].strip()

            if not name:
                raise ValidationError("Customer name is required.")

            return name

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

        def clean_name(self):
            name = self.cleaned_data["name"].strip()

            if not name:
                raise ValidationError("Site name is required.")

            return name

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

    def clean(self):
        cleaned_data = super().clean()

        download_mbps = cleaned_data.get("download_mbps")
        upload_mbps = cleaned_data.get("upload_mbps")
        ping_ms = cleaned_data.get("ping_ms")
        jitter_ms = cleaned_data.get("jitter_ms")
        isp = cleaned_data.get("isp")

        if isp:
            cleaned_data["isp"] = isp.strip()

        if download_mbps is not None and download_mbps < 0:
            self.add_error("download_mbps", "Download speed cannot be negative.")

        if upload_mbps is not None and upload_mbps < 0:
            self.add_error("upload_mbps", "Upload speed cannot be negative.")

        if ping_ms is not None and ping_ms < 0:
            self.add_error("ping_ms", "Ping cannot be negative.")

        if jitter_ms is not None and jitter_ms < 0:
            self.add_error("jitter_ms", "Jitter cannot be negative.")

        return cleaned_data