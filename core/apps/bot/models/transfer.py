from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class TransferOrder(AbstractBaseModel):
    STATUS = (
        ("pending", _("pending")),
        ("confirmed", _("confirmed")),
    )
    user = models.ForeignKey("BotUser", on_delete=models.SET_NULL, null=True, blank=False)
    service_type = models.CharField(_("serrvice type"), max_length=255)
    category = models.ForeignKey("CategoryModel", on_delete=models.SET_NULL, null=True)
    date = models.CharField(_("date"), max_length=255)
    passanger_count = models.CharField(_("passanger_count"), max_length=255)
    goods = models.CharField(_("goods"), max_length=255)
    status = models.CharField(_("status"), max_length=255, choices=STATUS, default="pending")
