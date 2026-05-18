from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Site(TimeStampedModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="sites",
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["customer__name", "name"]

    def __str__(self):
        return f"{self.customer.name} - {self.name}"

class SpeedTestResult(TimeStampedModel):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="speed_tests",
    )
    isp = models.CharField(max_length=100)
    download_mbps = models.DecimalField(max_digits=8, decimal_places=2)
    upload_mbps = models.DecimalField(max_digits=8, decimal_places=2)
    ping_ms = models.DecimalField(max_digits=8, decimal_places=2)
    jitter_ms = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    test_datetime = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-test_datetime"]

    def __str__(self):
        return f"{self.site} - {self.download_mbps} Mbps down"