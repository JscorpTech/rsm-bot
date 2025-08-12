from django.conf import settings
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from core.apps.bot.services import get_message, list_to_rely_button


def home():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(get_message("hotel")), KeyboardButton(get_message("transfer")))
    button.add(KeyboardButton(get_message("visa")), KeyboardButton(get_message("mini_tour")))
    button.add(KeyboardButton(get_message("contact")), KeyboardButton(get_message("change_lang")))
    return button


def hotel():
    return back(list_to_rely_button(settings.HOTEL_LOCATIONS))


def hotel_tariff():
    return back(list_to_rely_button(settings.HOTEL_TARIFF))


def back(button):
    button.add(KeyboardButton(get_message("back")))
    return button


def lang():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(get_message("uz")))
    button.add(KeyboardButton(get_message("en")))
    button.add(KeyboardButton(get_message("ru")))
    return back(button)


def phone():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(get_message("send_phone"), request_contact=True))
    return button


def mini_tour():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    return button


def transfer():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(get_message("standard")))
    button.add(KeyboardButton(get_message("comfort")))
    button.add(KeyboardButton(get_message("lux")))
    return back(button)
