from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.bot.models import Category, Services


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["id", "name", "key"]


@admin.register(Services)
class ServicesAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["id", "name"]
