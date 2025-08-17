from django.conf import settings
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from core.apps.bot.services import get_address_list, get_category_list
from core.apps.bot.services import get_message as _
from core.apps.bot.services import make_rely_button


def home():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("hotel")), KeyboardButton(_("transfer")))
    button.add(KeyboardButton(_("visa")), KeyboardButton(_("mini_tour")))
    button.add(KeyboardButton(_("contact")), KeyboardButton(_("change_lang")))
    return button


def hotel_locations():
    return back(make_rely_button(get_address_list("hotel"), translate=False))


def hotel_list(hotels):
    return back(make_rely_button(hotels, translate=False))


def hotel_detail():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("videos_images")))
    button.add(KeyboardButton(_("break")))
    return back(button)


def hotel_tariff():
    return back(make_rely_button(get_category_list("hotel"), translate=False))


def back(button=None):
    if button is None:
        button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("back")), KeyboardButton(_("back_home")))
    return button


def lang(back=True):
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("uz")))
    button.add(KeyboardButton(_("en")))
    button.add(KeyboardButton(_("ru")))
    if back:
        return back(button)
    return button


def phone():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("send_phone"), request_contact=True))
    return button


def mini_tour():
    return back(make_rely_button(settings.MINI_TOUR))


def transfer():
    return back(make_rely_button(settings.TRANSFER_SERVICE_TYPES))


def transfer_category():
    return back(make_rely_button(get_category_list("transfer"), translate=False))


def visa():
    return back(make_rely_button(settings.VISA_SERVICE_TYPES))
