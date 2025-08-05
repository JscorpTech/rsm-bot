from telebot.types import Message

from core.apps.bot.bot import bot
from core.apps.bot.services import get_message, get_or_create_user
from core.apps.bot.states.register import RegisterState


@bot.message_handler(commands=["start"])
def start(msg: Message):
    user, created = get_or_create_user(msg.chat.id)
    if not created and user.is_register:
        bot.send_message(msg.chat.id, get_message("re_start"))
        return
    bot.set_state(
        msg.from_user.id,
        RegisterState.full_name,
        chat_id=msg.chat.id,
    )
    bot.send_message(msg.chat.id, get_message("start"))
