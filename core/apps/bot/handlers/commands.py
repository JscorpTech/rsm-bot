from telebot.types import Message

from core.apps.bot import buttons
from core.apps.bot.bot import bot
from core.apps.bot.services import get_data, get_message, get_or_create_user, set_data

from . import pages


@bot.message_handler(commands=["start"])
def start(msg: Message):
    user, created = get_or_create_user(msg.chat.id)
    if not created and user.is_register:
        bot.send_message(
            msg.chat.id,
            get_message("home"),
            reply_markup=buttons.home(),
        )
        return
    get_or_create_user(msg.chat.id)
    set_data(msg.chat.id, "page", "change_lang")
    bot.send_message(msg.chat.id, get_message("start"))
    bot.send_message(
        msg.chat.id,
        get_message("select_lang"),
        reply_markup=buttons.lang(),
    )


@bot.message_handler(message="home")
def home(msg: Message):
    set_data(msg.chat.id, "page", "home")
    bot.send_message(
        msg.chat.id,
        get_message("home"),
        reply_markup=buttons.home(),
    )


@bot.message_handler(message="back")
def back(msg: Message):
    page = get_data(msg.chat.id, "page")
    if page in ["change_lang", "transfer"]:
        set_data(msg.chat.id, "page", "home")
        bot.send_message(
            msg.chat.id,
            get_message("home"),
            reply_markup=buttons.home(),
        )
    if page == "hotel":
        state = bot.get_state(msg.chat.id)
        match state:
            case "HotelState:location":
                home(msg)
            case "HotelState:tariff":
                pages.hotel_handler(msg)
