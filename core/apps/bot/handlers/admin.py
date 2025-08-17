from telebot.types import Message

from core.apps.bot.bot import bot
from core.apps.bot.services import get_message as _
from core.apps.bot.states import AdminState


@bot.message_handler(message="file_id")
def file_handler(msg: Message):
    bot.set_state(msg.chat.id, AdminState.file_id)
    bot.send_message(msg.chat.id, _("send_file"))


@bot.message_handler(state=AdminState.file_id, content_types=["photo"])
def file_id_photo_handler(msg: Message):
    file_id = msg.photo[-1].file_id
    bot.send_message(msg.chat.id, file_id)


@bot.message_handler(state=AdminState.file_id, content_types=["video"])
def file_id_video_handler(msg: Message):
    file_id = msg.video.file_id
    bot.send_message(msg.chat.id, file_id)
