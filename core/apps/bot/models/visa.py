from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class VisaOrder(AbstractBaseModel):

    STATUS = (
        ("pending", _("pending")),
        ("confirmed", _("confirmed")),
    )
    user = models.ForeignKey("BotUser", on_delete=models.SET_NULL, null=True, blank=False)
    full_name = models.CharField(_("full_name"), max_length=255)
    passport_front = models.FileField(_("passport front"), upload_to="passports/", null=True)
    passport_front_file_id = models.CharField(_("passport_front_file_id"), max_length=255, null=True, blank=True)
    passport_back = models.FileField(_("passport back"), upload_to="passports/", null=True)
    passport_back_file_id = models.CharField(_("passport_back_file_id"), max_length=255, null=True, blank=True)
    date = models.CharField(_("date"), max_length=255)
    nationality = models.CharField(_("nationality"), max_length=255, null=True)
    birth_date = models.CharField(_("birth date"), max_length=255)
    service = models.CharField(_("service"), max_length=255)
    status = models.CharField(_("status"), max_length=255, choices=STATUS, default="pending")
