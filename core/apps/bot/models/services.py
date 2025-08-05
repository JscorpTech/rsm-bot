from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class Category(AbstractBaseModel):
    key = models.CharField(_("key"), unique=True, max_length=255)
    name = models.CharField(_("name"), max_length=255)
    desc = models.TextField(_("desc"))
    child = models.ManyToManyField(
        "Category",
        verbose_name=_("chield"),
        related_name="parent",
    )

    class Meta:
        db_table = "categories"
        verbose_name = _("categories")
        verbose_name_plural = _("services")


class Services(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    categories = models.ManyToManyField(
        "Category",
        verbose_name=_("category"),
    )

    class Meta:
        db_table = "services"
        verbose_name = _("services")
        verbose_name_plural = _("services")
