from typing import Optional, TypeVar, cast

from django.core.cache import cache
from django.utils import translation
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from core.apps.bot.models import AddressModel, BotUser, CategoryModel, Messages

T = TypeVar("T")


def get_category_list(service):
    return CategoryModel.objects.filter(service=service).values_list("name", flat=True)


def get_address_list(service):
    return AddressModel.objects.filter(service=service).values_list("name", flat=True)


def make_rely_button(data, translate=True):
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data:
        if translate:
            text = get_message(item)
        else:
            text = item
        if text is None:
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


def get_message_key(value, default=None) -> Optional[str]:
    message = Messages.objects.filter(value=value)
    if not message.exists():
        return default or f"message is not found message: {value}"
    return message.first().key  # type: ignore


def get_message(key, default: T | None = None) -> str | T:
    message = Messages.objects.filter(key=key)
    if not message.exists():
        return default or f"message is not found key: {key}"
    return message.first().value  # type: ignore


def update_lang(chat_id, lang):
    user = get_user(chat_id)
    if user is None:
        return
    user = cast(BotUser, user)
    user.lang = lang
    user.save()
    translation.activate(lang)
