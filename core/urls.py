from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
    path("customers/new/", views.CustomerCreateView.as_view(), name="customer_create"),
    path("customers/<int:pk>/", views.CustomerDetailView.as_view(), name="customer_detail"),
    path("customers/<int:pk>/edit/", views.CustomerUpdateView.as_view(), name="customer_update"),
    path("customers/<int:pk>/delete/", views.CustomerDeleteView.as_view(), name="customer_delete"),
]