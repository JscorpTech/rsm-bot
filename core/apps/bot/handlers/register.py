from telebot.types import Message

from core.apps.bot.bot import bot
from core.apps.bot.states.register import RegisterState


@bot.message_handler(state=RegisterState.full_name, content_types=["text"])
def full_name(msg: Message):
    bot.send_message(msg.chat.id, "Ismingiz qabul qilindi")
    bot.set_state(msg.from_user.id, RegisterState.phone)
    with bot.retrieve_data(msg.chat.id) as data:
        data["full_name"] = msg.text


@bot.message_handler(state=RegisterState.phone)
def phone(msg: Message):
    bot.send_message(msg.chat.id, "Telefon no'mer qabul qilindi")
    with bot.retrieve_data(msg.chat.id) as data:
        bot.send_message(msg.chat.id, f"{data['full_name']} -> {msg.text}")
