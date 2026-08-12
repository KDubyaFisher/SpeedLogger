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

class SiteOwnershipTests(TestCase):
    def setUp(self):
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

        self.site_a = Site.objects.create(
            customer=self.customer_a,
            name="User A Site",
        )
        self.site_b = Site.objects.create(
            customer=self.customer_b,
            name="User B Site",
        )

    def test_site_list_only_shows_logged_in_users_sites(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(reverse("core:site_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User A Site")
        self.assertNotContains(response, "User B Site")

    def test_user_cannot_view_another_users_site(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(
            reverse("core:site_detail", args=[self.site_b.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_update_another_users_site(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse("core:site_update", args=[self.site_b.pk]),
            {
                "customer": self.customer_b.pk,
                "name": "Changed Site",
            },
        )

        self.assertEqual(response.status_code, 404)

        self.site_b.refresh_from_db()
        self.assertEqual(self.site_b.name, "User B Site")

    def test_user_cannot_delete_another_users_site(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse("core:site_delete", args=[self.site_b.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Site.objects.filter(pk=self.site_b.pk).exists()
        )

    def test_site_form_only_contains_logged_in_users_customers(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(reverse("core:site_create"))

        customer_queryset = response.context["form"].fields[
            "customer"
        ].queryset

        self.assertIn(self.customer_a, customer_queryset)
        self.assertNotIn(self.customer_b, customer_queryset)

    def test_user_cannot_create_site_for_another_users_customer(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse("core:site_create"),
            {
                "customer": self.customer_b.pk,
                "name": "Unauthorized Site",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Site.objects.filter(name="Unauthorized Site").exists()
        )

    def test_user_can_create_site_for_owned_customer(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse("core:site_create"),
            {
                "customer": self.customer_a.pk,
                "name": "New Site",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:site_list"),
        )

        site = Site.objects.get(name="New Site")
        self.assertEqual(site.customer, self.customer_a)

class SpeedTestOwnershipTests(TestCase):
    def setUp(self):
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

        self.site_a = Site.objects.create(
            customer=self.customer_a,
            name="User A Site",
        )
        self.site_b = Site.objects.create(
            customer=self.customer_b,
            name="User B Site",
        )

        self.speed_test_a = SpeedTestResult.objects.create(
            site=self.site_a,
            isp="User A ISP",
            download_mbps=Decimal("500.00"),
            upload_mbps=Decimal("50.00"),
            ping_ms=Decimal("10.00"),
            jitter_ms=Decimal("2.00"),
            test_datetime=timezone.now(),
        )

        self.speed_test_b = SpeedTestResult.objects.create(
            site=self.site_b,
            isp="User B ISP",
            download_mbps=Decimal("300.00"),
            upload_mbps=Decimal("30.00"),
            ping_ms=Decimal("20.00"),
            jitter_ms=Decimal("4.00"),
            test_datetime=timezone.now(),
        )

    def test_speed_test_list_only_shows_logged_in_users_records(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(reverse("core:speedtest_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User A ISP")
        self.assertNotContains(response, "User B ISP")

    def test_user_cannot_view_another_users_speed_test(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(
            reverse(
                "core:speedtest_detail",
                args=[self.speed_test_b.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_update_another_users_speed_test(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse(
                "core:speedtest_update",
                args=[self.speed_test_b.pk],
            ),
            {
                "site": self.site_b.pk,
                "isp": "Changed ISP",
                "download_mbps": "100.00",
                "upload_mbps": "10.00",
                "ping_ms": "5.00",
                "jitter_ms": "1.00",
                "test_datetime": timezone.now().strftime(
                    "%Y-%m-%dT%H:%M"
                ),
            },
        )

        self.assertEqual(response.status_code, 404)

        self.speed_test_b.refresh_from_db()
        self.assertEqual(self.speed_test_b.isp, "User B ISP")

    def test_user_cannot_delete_another_users_speed_test(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse(
                "core:speedtest_delete",
                args=[self.speed_test_b.pk],
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            SpeedTestResult.objects.filter(
                pk=self.speed_test_b.pk
            ).exists()
        )

    def test_speed_test_form_only_contains_logged_in_users_sites(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(
            reverse("core:speedtest_create")
        )

        site_queryset = response.context["form"].fields[
            "site"
        ].queryset

        self.assertIn(self.site_a, site_queryset)
        self.assertNotIn(self.site_b, site_queryset)

    def test_user_cannot_create_speed_test_for_another_users_site(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse("core:speedtest_create"),
            {
                "site": self.site_b.pk,
                "isp": "Unauthorized ISP",
                "download_mbps": "200.00",
                "upload_mbps": "20.00",
                "ping_ms": "15.00",
                "jitter_ms": "3.00",
                "test_datetime": timezone.now().strftime(
                    "%Y-%m-%dT%H:%M"
                ),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            SpeedTestResult.objects.filter(
                isp="Unauthorized ISP"
            ).exists()
        )

    def test_user_can_create_speed_test_for_owned_site(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.post(
            reverse("core:speedtest_create"),
            {
                "site": self.site_a.pk,
                "isp": "New ISP",
                "download_mbps": "600.00",
                "upload_mbps": "60.00",
                "ping_ms": "8.00",
                "jitter_ms": "1.50",
                "test_datetime": timezone.now().strftime(
                    "%Y-%m-%dT%H:%M"
                ),
            },
        )

        self.assertRedirects(
            response,
            reverse("core:speedtest_list"),
        )

        speed_test = SpeedTestResult.objects.get(
            isp="New ISP"
        )
        self.assertEqual(speed_test.site, self.site_a)

    def test_search_only_returns_logged_in_users_records(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(
            reverse("core:speedtest_search"),
            {"q": "ISP"},
        )

        self.assertContains(response, "User A ISP")
        self.assertNotContains(response, "User B ISP")

    def test_report_only_returns_logged_in_users_records(self):
        self.client.login(
            username="user_a",
            password="testpass123",
        )

        response = self.client.get(
            reverse("core:speedtest_report")
        )

        self.assertContains(response, "User A ISP")
        self.assertNotContains(response, "User B ISP")

class SignupTests(TestCase):
    def test_signup_page_is_available_to_anonymous_users(self):
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Account")

    def test_valid_signup_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse("core:home"),
        )

        user = User.objects.get(username="newuser")

        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(response.context["user"], user)

    def test_signup_rejects_duplicate_username(self):
        User.objects.create_user(
            username="existinguser",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("signup"),
            {
                "username": "existinguser",
                "email": "different@example.com",
                "password1": "StrongPass456!",
                "password2": "StrongPass456!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.filter(username="existinguser").count(),
            1,
        )

    def test_signup_rejects_duplicate_email(self):
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "EXISTING@example.com",
                "password1": "StrongPass456!",
                "password2": "StrongPass456!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="newuser").exists()
        )
        self.assertContains(
            response,
            "An account with this email address already exists.",
        )

    def test_signup_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "DifferentPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="newuser").exists()
        )

    def test_new_user_starts_with_empty_customer_workspace(self):
        existing_user = User.objects.create_user(
            username="existinguser",
            password="StrongPass123!",
        )

        Customer.objects.create(
            owner=existing_user,
            name="Existing Customer",
        )

        self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        response = self.client.get(
            reverse("core:customer_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Existing Customer")