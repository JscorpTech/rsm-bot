from telebot.types import Message

from core.apps.bot import buttons
from core.apps.bot.bot import bot
from core.apps.bot.services import get_message as _
from core.apps.bot.services import get_user, set_data
from core.apps.bot.states import RegisterState


@bot.message_handler(state=RegisterState.full_name)
def first_name_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["full_name"] = msg.text
    bot.set_state(msg.from_user.id, RegisterState.phone, msg.chat.id)
    bot.send_message(msg.chat.id, _("enter_phone"), reply_markup=buttons.phone())


@bot.message_handler(state=RegisterState.phone, content_types=["contact"])
def phone_handler(msg: Message):
    phone = msg.contact.phone_number
    with bot.retrieve_data(msg.chat.id) as data:
        full_name = data["full_name"]
        user = get_user(msg.chat.id)
        user.full_name = full_name
        user.phone = phone
        user.is_register = True
        user.save()
    set_data(msg.chat.id, "page", "home")
    bot.delete_state(msg.chat.id)
    bot.send_message(
        msg.chat.id,
        _("home"),
        reply_markup=buttons.home(),
    )
