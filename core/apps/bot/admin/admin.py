from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, TabularInline

from core.apps.bot.models import AddressModel, CategoryModel, HotelModel, VisaOrder
from core.apps.bot.models.hotel import File, HotelOrder
from core.apps.bot.models.mini_tour import MiniTourOrder, PackageModel
from core.apps.bot.models.transfer import TransferOrder


class HotelInline(TabularInline):
    model = File
    tab = True
    extra = 1


@admin.register(HotelModel)
class HotelAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["name"]
    autocomplete_fields = ["category", "location"]
    inlines = [HotelInline]


@admin.register(AddressModel)
class AddressAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(CategoryModel)
class CategoryAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["name"]
    search_fields = ["fields"]


@admin.register(VisaOrder)
class VisaOrderAdmin(ModelAdmin):
    list_display = ["id", "full_name"]


@admin.register(TransferOrder)
class VisaOrderAdmin(ModelAdmin):
    list_display = ["id", "user__full_name", "status"]


@admin.register(MiniTourOrder)
class MiniTourOrderAdmin(ModelAdmin):
    list_display = ["id", "user__full_name"]


@admin.register(PackageModel)
class PackageAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["id", "name", "file"]


@admin.register(HotelOrder)
class HotelOrderAdmin(ModelAdmin):
    list_display = [
        "id",
        "location__name",
        "category__name",
        "status",
    ]
