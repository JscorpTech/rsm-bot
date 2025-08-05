from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.bot.models import BotUser, Messages


@admin.register(BotUser)
class BotUserAdmin(ModelAdmin):
    list_display = ["chat_id"]


@admin.register(Messages)
class MessagesAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["key", "value"]
