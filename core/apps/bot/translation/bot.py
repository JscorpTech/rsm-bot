from modeltranslation.translator import TranslationOptions, register

from core.apps.bot.models import Messages


@register(Messages)
class MessageTranslation(TranslationOptions):
    fields = ["value"]

