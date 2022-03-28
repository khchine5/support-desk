from django import template
from supportdesk.models import Request

register = template.Library()


@register.filter
def button_type(request_status):
    if request_status == Request.RequestStatus.COMPLETED:
        return "success"
    if request_status == Request.RequestStatus.CREATED:
        return "info"
    if request_status == Request.RequestStatus.ONPROGRESS:
        return "primary"