from django.contrib import admin

from .models import Customer, Site


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_name", "contact_email", "phone", "created_at")
    search_fields = ("name", "contact_name", "contact_email")


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "customer", "city", "state", "created_at")
    search_fields = ("name", "customer__name", "city", "state")
    list_filter = ("state",)