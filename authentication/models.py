from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


class SupportUser(AbstractUser):
    class SupportUserRole(models.IntegerChoices):
        AGENT = 0, _("Agent")
        CUSTOMER = 1, _("Customer")
    role = models.PositiveSmallIntegerField(
        verbose_name=_("Role"),
        choices=SupportUserRole.choices,
        default=SupportUserRole.CUSTOMER,
    )

    @property
    def is_customer(self):
        return self.role == SupportUser.SupportUserRole.CUSTOMER

    @property
    def requests_count(self):
        return self.myrequests.count()
