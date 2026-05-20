from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import SpeedTestResultForm
from .models import Customer, Site, SpeedTestResult


class SpeedTestValidationTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer")
        self.site = Site.objects.create(
            customer=self.customer,
            name="Main Office",
            city="Austin",
            state="TX",
        )

    def test_speed_test_form_rejects_negative_download_speed(self):
        form_data = {
            "site": self.site.id,
            "isp": "Test ISP",
            "download_mbps": "-10.00",
            "upload_mbps": "50.00",
            "ping_ms": "12.00",
            "jitter_ms": "2.00",
            "test_datetime": timezone.now().strftime("%Y-%m-%dT%H:%M"),
            "notes": "Invalid negative download test.",
        }

        form = SpeedTestResultForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("download_mbps", form.errors)


class SpeedTestReportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

        self.customer = Customer.objects.create(name="Test Customer")
        self.site = Site.objects.create(
            customer=self.customer,
            name="Main Office",
            city="Austin",
            state="TX",
        )

        SpeedTestResult.objects.create(
            site=self.site,
            isp="Test ISP",
            download_mbps=Decimal("500.00"),
            upload_mbps=Decimal("50.00"),
            ping_ms=Decimal("10.00"),
            jitter_ms=Decimal("2.00"),
            test_datetime=timezone.now(),
            notes="Report test record.",
        )

    def test_report_page_displays_report_title_for_authenticated_user(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("core:speedtest_report"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Speed Test Report")
        self.assertContains(response, "Test ISP")