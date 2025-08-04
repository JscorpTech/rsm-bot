from telebot.types import Message

from core.apps.bot.bot import bot
from core.apps.bot.states.register import RegisterState


@bot.message_handler(commands=["start"])
def start(msg: Message):
    bot.set_state(
        msg.from_user.id,
        RegisterState.full_name,
        chat_id=msg.chat.id,
    )
    bot.send_message(msg.chat.id, "Salom")


@bot.message_handler(func=lambda m: m.text == "salom")
def phone(message: Message):
    bot.send_message(message.chat.id, "salom")
