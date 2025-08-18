from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class HotelModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    desc = models.TextField(_("desc"))
    location = models.ManyToManyField("AddressModel")
    category = models.ManyToManyField("CategoryModel")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotel")
        db_table = "hotels"


class File(AbstractBaseModel):
    FILE_TYPES = (
        ("image", _("image")),
        ("video", _("video")),
    )
    hotel = models.ForeignKey("HotelModel", on_delete=models.CASCADE, related_name="files")
    file = models.FileField(_("file"), upload_to="hotel/", null=True, blank=True)
    file_type = models.CharField(_("file type"), max_length=255, choices=FILE_TYPES, default="video")
    file_id = models.CharField(_("file id"), max_length=255, null=True, blank=True)


class HotelOrder(AbstractBaseModel):

    STATUS = (
        ("pending", _("pending")),
        ("confirmed", _("confirmed")),
    )
    user = models.ForeignKey("BotUser", on_delete=models.SET_NULL, null=True, blank=False)
    location = models.ForeignKey("AddressModel", on_delete=models.SET_NULL, null=True, blank=False)
    category = models.ForeignKey("CategoryModel", on_delete=models.SET_NULL, null=True, blank=False)
    arrival_date = models.CharField(_("arrival_date"), max_length=255)
    departure_date = models.CharField(_("departure_date"), max_length=255)
    rooms = models.CharField(_("rooms"), max_length=255)
    hotel = models.ForeignKey("HotelModel", on_delete=models.SET_NULL, null=True, blank=False)
    power_type = models.CharField(_("power type"), max_length=255, default="RO")
    transfer = models.BooleanField(_("transfer"), default=False)
    status = models.CharField(_("status"), choices=STATUS, max_length=255, default="pending")
