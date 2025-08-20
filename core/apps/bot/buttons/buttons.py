from django.conf import settings
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from core.apps.bot.models.mini_tour import PackageModel
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


def yes_no():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("yes")), KeyboardButton(_("no")))
    return back(button)


def power_type():
    return back(make_rely_button(settings.POWER_TYPES))


def lang(is_back=True):
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("uz")))
    button.add(KeyboardButton(_("en")))
    button.add(KeyboardButton(_("ru")))
    if is_back:
        return back(button)
    return button


def phone():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("send_phone"), request_contact=True))
    return button


def mini_tour():
    return back(make_rely_button(get_address_list("mini_tour"), translate=False))


def mini_tour_packages():
    return back(make_rely_button(PackageModel.objects.all().values_list("name", flat=True), translate=False))


def mini_tour_detail():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(KeyboardButton(_("break")))
    return back(button)


def transfer():
    return back(make_rely_button(settings.TRANSFER_SERVICE_TYPES))


def transfer_category():
    return back(make_rely_button(get_category_list("transfer"), translate=False))


def visa():
    return back(make_rely_button(settings.VISA_SERVICE_TYPES))
