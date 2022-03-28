from django.utils.translation import gettext as _

from django.db import models
from django.contrib.auth import get_user_model
from authentication.models import SupportUser


class Request(models.Model):
    class RequestStatus(models.IntegerChoices):
        CREATED = 0, _("Created")
        ONPROGRESS = 1, _("On progress")
        COMPLETED = 2, _("Completed")

    customer = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Customer"),
        on_delete=models.CASCADE,
        related_name="myrequests",
        limit_choices_to={"role": SupportUser.SupportUserRole.CUSTOMER},
    )
    summary = models.CharField(verbose_name=_("Summary"), max_length=500)
    description = models.TextField(verbose_name=_("Description"))
    high_priority = models.BooleanField(_("Flag as high priority"))
    agent = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="my_assigned_requests",
        limit_choices_to={"role": SupportUser.SupportUserRole.AGENT},
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=_("Status"),
        choices=RequestStatus.choices,
        default=RequestStatus.CREATED,
    )
    created_on = models.DateTimeField(verbose_name=_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name=_("Updated on"), auto_now=True)

    def mark_complete(self):
        self.status = self.RequestStatus.COMPLETED
        self.save()

    @property
    def is_completed(self):
        return self.status == self.RequestStatus.COMPLETED

    def __str__(self) -> str:
        return self.summary
