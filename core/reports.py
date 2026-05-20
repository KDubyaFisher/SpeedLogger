from abc import ABC, abstractmethod
from django.utils import timezone

from .models import SpeedTestResult


class BaseReportGenerator(ABC):
    def __init__(self, queryset=None):
        self.queryset = queryset
        self.generated_at = timezone.now()

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_columns(self):
        pass

    @abstractmethod
    def get_rows(self):
        pass


class SpeedTestReportGenerator(BaseReportGenerator):
    def __init__(self, queryset=None):
        if queryset is None:
            queryset = SpeedTestResult.objects.select_related("site", "site__customer")
        super().__init__(queryset)

    def get_title(self):
        return "Speed Test Report"

    def get_columns(self):
        return [
            "Customer",
            "Site",
            "ISP",
            "Download Mbps",
            "Upload Mbps",
            "Ping ms",
            "Jitter ms",
            "Test Date",
        ]

    def get_rows(self):
        rows = []

        for speed_test in self.queryset:
            rows.append([
                speed_test.site.customer.name,
                speed_test.site.name,
                speed_test.isp,
                speed_test.download_mbps,
                speed_test.upload_mbps,
                speed_test.ping_ms,
                speed_test.jitter_ms or "—",
                speed_test.test_datetime,
            ])

        return rows