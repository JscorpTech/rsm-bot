from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.bot.models import AddressModel, CategoryModel, HotelModel


@admin.register(HotelModel)
class HotelAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["name"]
    autocomplete_fields = ["category", "location"]


@admin.register(AddressModel)
class AddressAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(CategoryModel)
class CategoryAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["name"]
    search_fields = ["fields"]
