from typing import Optional

from django.core.cache import cache
from django.utils import translation
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from core.apps.bot.models import AddressModel, BotUser, CategoryModel, Messages


def get_category_list(service):
    return CategoryModel.objects.filter(service=service).values_list("name", flat=True)


def get_address_list(service):
    return AddressModel.objects.filter(service=service).values_list("name", flat=True)


def make_rely_button(data, translate=True):
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data:
        if translate:
            text = _(item)
        else:
            text = item
        button.add(KeyboardButton(text))
    return button


def get_user(chat_id):
    user = BotUser.objects.filter(chat_id=chat_id)
    if not user.exists():
        return None
    return user.first()


def get_or_create_user(chat_id):
    return BotUser.objects.get_or_create(chat_id=chat_id)


def set_data(chat_id, key, value):
    return cache.set(f"user:{chat_id}:{key}", value)


def get_data(chat_id, key, default=None):
    return cache.get(f"user:{chat_id}:{key}", default)


def get_message_key(message, default=None) -> Optional[str]:
    message = Messages.objects.filter(value=message)
    if not message.exists():
        if default is None:
            default = f"message is not found message: {message}"
        return default
    return message.first().key


def get_message(key, default=None) -> Optional[str]:
    message = Messages.objects.filter(key=key)
    if not message.exists():
        if default is None:
            default = f"message is not found key: {key}"
        return default
    return message.first().value


def update_lang(chat_id, lang):
    user = get_user(chat_id)
    user.lang = lang
    user.save()
    translation.activate(lang)
