from modeltranslation.translator import TranslationOptions, register

from core.apps.bot.models import Category, Services


@register(Category)
class CateogryTranslation(TranslationOptions):
    fields = ["name", "desc"]


@register(Services)
class ServicesTranslation(TranslationOptions):
    fields = ["name"]
