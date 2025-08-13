from modeltranslation.translator import TranslationOptions, register

from core.apps.bot.models import AddressModel, CategoryModel, HotelModel


@register(HotelModel)
class HotelTranslation(TranslationOptions):
    fields = ["name", "desc"]


@register(CategoryModel)
class categoryTranslation(TranslationOptions):
    fields = ["name"]


@register(AddressModel)
class AddressTranslation(TranslationOptions):
    fields = ["name"]
