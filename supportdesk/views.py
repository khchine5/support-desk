from typing import List

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from supportdesk.models import Request


def check_agent(user):
    return user.role == get_user_model().SupportUserRole.AGENT


def check_customer(user):
    return user.role == get_user_model().SupportUserRole.CUSTOMER


class PlaceholderHome(TemplateView):
    template_name = "supportdesk/placeholder.html"


class AgentPermission(LoginRequiredMixin):
    """Verify that the current user has the AGENT role."""

    def dispatch(self, request, *args, **kwargs):
        if not check_agent(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomerPermission(LoginRequiredMixin):
    """Verify that the current user has the CUSTOMER role."""

    def dispatch(self, request, *args, **kwargs):
        if not check_customer(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AgentMyRequestMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user == self.object.agent:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CreateRequest(CustomerPermission, CreateView):
    model = Request
    fields = ["summary", "description", "high_priority"]
    success_url = reverse_lazy("requests-list")

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)


class RequestsView(LoginRequiredMixin, ListView):
    customer_template_name = "supportdesk/customer_requests.html"
    agent_template_name = "supportdesk/agent_requests.html"
    model = Request

    def get_template_names(self) -> List[str]:
        if self.request.user.is_customer:
            return [self.customer_template_name]
        return [self.agent_template_name]

    def get_queryset(self):
        if self.request.user.is_customer:
            return super().get_queryset().filter(customer=self.request.user)
        return (
            super()
            .get_queryset()
            .filter(agent=self.request.user)
            .exclude(status=Request.RequestStatus.COMPLETED)
        )


class RequestDetailView(AgentPermission, AgentMyRequestMixin, DetailView):
    model = Request


class RequestUpdateView(AgentPermission, AgentMyRequestMixin, UpdateView):
    model = Request
    fields = ["agent"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("requests-list")


@user_passes_test(check_agent)
def mark_request_compelete(request, pk):
    Request.objects.get(pk=pk).mark_complete()
    return redirect("requests-list")
