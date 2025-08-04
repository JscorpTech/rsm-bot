from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class BotUser(AbstractBaseModel):
    chat_id = models.CharField(verbose_name=_("chat id"), max_length=255)
