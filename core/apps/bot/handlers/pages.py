from django.conf import settings
from telebot.types import Message

from core.apps.bot import buttons
from core.apps.bot.bot import bot
from core.apps.bot.services import get_data, get_message, get_message_key, get_user, set_data, update_lang
from core.apps.bot.states import HotelState, RegisterState


@bot.message_handler(message="hotel")
def hotel_handler(msg: Message):
    set_data(msg.chat.id, "page", "hotel")
    bot.set_state(msg.chat.id, HotelState.location)
    bot.send_message(
        msg.chat.id,
        get_message("hotel"),
        reply_markup=buttons.hotel(),
    )


@bot.message_handler(
    state=HotelState.location,
    message=settings.HOTEL_LOCATIONS,
)
def hotel_location_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["hotel_location"] = get_message_key(msg.text)
    bot.set_state(msg.chat.id, HotelState.tariff)
    bot.send_message(
        msg.chat.id,
        get_message("select_hotel_tariff"),
        reply_markup=buttons.hotel_tariff(),
    )


@bot.message_handler(state=HotelState.tariff, messages=settings.HOTEL_TARIFF)
@bot.message_handler(message="transfer")
def transfer_handler(msg: Message):
    set_data(msg.chat.id, "page", "transfer")
    bot.send_message(
        msg.chat.id,
        get_message("transfer_desc"),
        reply_markup=buttons.transfer(),
    )


@bot.message_handler(message="change_lang")
def change_lang(msg: Message):
    set_data(msg.chat.id, "page", "change_lang")
    bot.send_message(
        msg.chat.id,
        get_message("select_lang"),
        reply_markup=buttons.lang(),
    )


@bot.message_handler(message=["uz", "en", "ru"])
def select_lang(msg: Message):
    set_data(msg.chat.id, "page", "home")
    update_lang(msg.chat.id, get_message_key(msg.text, "uz"))
    user = get_user(msg.chat.id)
    if not user.is_register:
        set_data(msg.chat.id, "page", "register")
        bot.set_state(msg.from_user.id, RegisterState.full_name, msg.chat.id)
        bot.send_message(msg.chat.id, get_message("enter_first_name"))
        return
    bot.send_message(
        msg.chat.id,
        get_message("home"),
        reply_markup=buttons.home(),
    )
