from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import SpeedTestResultForm
from .models import Customer, Site, SpeedTestResult


class SpeedTestValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.customer = Customer.objects.create(
            owner=self.user,
            name="Test Customer",
        )
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

        self.customer = Customer.objects.create(
            owner=self.user,
            name="Test Customer",
        )
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

class CustomerOwnershipTests(TestCase):
    def setUp(self):
        # Create two separate users so we can verify that data is isolated
        # between accounts.
        self.user_a = User.objects.create_user(
            username="user_a",
            password="testpass123",
        )

        self.user_b = User.objects.create_user(
            username="user_b",
            password="testpass123",
        )

        self.customer_a = Customer.objects.create(
            owner=self.user_a,
            name="User A Customer",
        )

        self.customer_b = Customer.objects.create(
            owner=self.user_b,
            name="User B Customer",
        )

    def test_customer_list_only_shows_logged_in_users_customers(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(reverse("core:customer_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User A Customer")
        self.assertNotContains(response, "User B Customer")

    def test_customer_create_assigns_logged_in_user_as_owner(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse("core:customer_create"),
            {
                "name": "New Customer",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:customer_list"),
        )

        customer = Customer.objects.get(name="New Customer")

        self.assertEqual(customer.owner, self.user_a)

    def test_user_cannot_view_another_users_customer(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(
            reverse(
                "core:customer_detail",
                args=[self.customer_b.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_update_another_users_customer(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse(
                "core:customer_update",
                args=[self.customer_b.pk],
            ),
            {
                "name": "Changed By User A",
            },
        )

        self.assertEqual(response.status_code, 404)

        self.customer_b.refresh_from_db()

        self.assertEqual(
            self.customer_b.name,
            "User B Customer",
        )

    def test_user_cannot_delete_another_users_customer(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse(
                "core:customer_delete",
                args=[self.customer_b.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Customer.objects.filter(
                pk=self.customer_b.pk,
            ).exists()
        )