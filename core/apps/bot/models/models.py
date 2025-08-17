from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class CategoryModel(AbstractBaseModel):
    SERVICES = (
        ("hotel", _("hotel")),
        ("transfer", _("transfer")),
        ("mini_tour", _("mini_tour")),
    )
    name = models.CharField(_("name"), max_length=255)
    desc = models.TextField(_("desc"), null=True, blank=True)
    service = models.CharField(
        _("service"),
        max_length=255,
        choices=SERVICES,
        default="hotel",
    )

    def __str__(self) -> str:
        return self.name

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

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Address")
        db_table = "addresses"
