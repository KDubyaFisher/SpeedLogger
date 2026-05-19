from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CustomerForm, SiteForm
from .models import Customer, Site

@login_required
def home(request):
    return render(request, "core/home.html")


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "core/customer_list.html"
    context_object_name = "customers"


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "core/customer_detail.html"
    context_object_name = "customer"


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "core/customer_form.html"
    success_url = reverse_lazy("core:customer_list")


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "core/customer_form.html"
    success_url = reverse_lazy("core:customer_list")


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = "core/customer_confirm_delete.html"
    success_url = reverse_lazy("core:customer_list")

class SiteListView(LoginRequiredMixin, ListView):
    model = Site
    template_name = "core/site_list.html"
    context_object_name = "sites"


class SiteDetailView(LoginRequiredMixin, DetailView):
    model = Site
    template_name = "core/site_detail.html"
    context_object_name = "site"


class SiteCreateView(LoginRequiredMixin, CreateView):
    model = Site
    form_class = SiteForm
    template_name = "core/site_form.html"
    success_url = reverse_lazy("core:site_list")


class SiteUpdateView(LoginRequiredMixin, UpdateView):
    model = Site
    form_class = SiteForm
    template_name = "core/site_form.html"
    success_url = reverse_lazy("core:site_list")


class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = Site
    template_name = "core/site_confirm_delete.html"
    success_url = reverse_lazy("core:site_list")