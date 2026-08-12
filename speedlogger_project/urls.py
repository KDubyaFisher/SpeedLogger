from django.contrib import admin
from django.urls import include, path

from core.views import SignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/signup/",
        SignupView.as_view(),
        name="signup",
    ),
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
    path("", include("core.urls")),
]