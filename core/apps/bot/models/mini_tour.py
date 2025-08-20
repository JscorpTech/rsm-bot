from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class PackageModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    file = models.FileField(_("file"), upload_to="package")
    desc = models.TextField(_("desc"), null=True)


class MiniTourOrder(AbstractBaseModel):
    STATUS = (
        ("pending", _("pending")),
        ("confirmed", _("confirmed")),
    )
    user = models.ForeignKey("BotUser", on_delete=models.SET_NULL, null=True, blank=False)
    package = models.ForeignKey("PackageModel", on_delete=models.SET_NULL, null=True, blank=False)
    address = models.ForeignKey("AddressModel", on_delete=models.SET_NULL, null=True, blank=False)
    status = models.CharField(_("status"), max_length=255, choices=STATUS, default="pending")
