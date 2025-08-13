from telebot.types import Message

from core.apps.bot import buttons
from core.apps.bot.bot import bot
from core.apps.bot.services import get_message as _
from core.apps.bot.services import get_or_create_user, set_data


@bot.message_handler(commands=["start"])
def start(msg: Message):
    user, created = get_or_create_user(msg.chat.id)
    if not created and user.is_register:
        bot.send_message(
            msg.chat.id,
            _("home"),
            reply_markup=buttons.home(),
        )
        return
    get_or_create_user(msg.chat.id)
    set_data(msg.chat.id, "page", "change_lang")
    bot.send_message(msg.chat.id, _("start"))
    bot.send_message(
        msg.chat.id,
        _("select_lang"),
        reply_markup=buttons.lang(),
    )


@bot.message_handler(message="home")
def home(msg: Message):
    set_data(msg.chat.id, "page", "home")
    bot.send_message(
        msg.chat.id,
        _("home"),
        reply_markup=buttons.home(),
    )
