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


class CategoryModel(AbstractBaseModel):
    SERVICES = (
        ("hotel", _("hotel")),
        ("transfer", _("transfer")),
        ("mini_tour", _("mini_tour")),
    )
    name = models.CharField(_("name"), max_length=255)
    service = models.CharField(
        _("service"),
        max_length=255,
        choices=SERVICES,
        default="hotel",
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Category")
        db_table = "categories"


class AddressModel(AbstractBaseModel):
    SERVICES = (
        ("hotel", _("hotel")),
        ("transfer", _("transfer")),
        ("mini_tour", _("mini_tour")),
    )

    name = models.CharField(_("name"), max_length=255)
    service = models.CharField(
        _("service"),
        max_length=255,
        default="hotel",
        choices=SERVICES,
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Address")
        db_table = "addresses"
