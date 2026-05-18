from django.contrib import admin

from .models import Customer, Site, SpeedTestResult

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_name", "contact_email", "phone", "created_at")
    search_fields = ("name", "contact_name", "contact_email")


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "customer", "city", "state", "created_at")
    search_fields = ("name", "customer__name", "city", "state")
    list_filter = ("state",)

@admin.register(SpeedTestResult)
class SpeedTestResultAdmin(admin.ModelAdmin):
    list_display = (
        "site",
        "isp",
        "download_mbps",
        "upload_mbps",
        "ping_ms",
        "jitter_ms",
        "test_datetime",
        "created_at",
    )
    search_fields = (
        "site__name",
        "site__customer__name",
        "isp",
        "notes",
    )
    list_filter = ("isp", "test_datetime")