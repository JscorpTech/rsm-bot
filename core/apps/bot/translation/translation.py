from modeltranslation.translator import TranslationOptions, register

from core.apps.bot.models import AddressModel, CategoryModel, HotelModel
from core.apps.bot.models.mini_tour import PackageModel


@register(HotelModel)
class HotelTranslation(TranslationOptions):
    fields = ["name", "desc"]


@register(CategoryModel)
class categoryTranslation(TranslationOptions):
    fields = ["name", "desc"]


@register(PackageModel)
class PackageTranslation(TranslationOptions):
    fields = ["name", "desc"]


@register(AddressModel)
class AddressTranslation(TranslationOptions):
    fields = ["name"]
