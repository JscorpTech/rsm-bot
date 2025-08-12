from telebot import custom_filters

from core.apps.bot.services import get_data, get_message


class MessageFilter(custom_filters.AdvancedCustomFilter):
    key = "message"

    def check(self, message, data):
        if type(data) in [list, tuple]:
            for msg in data:
                if message.text == get_message(msg):
                    return True
            return False
        return message.text == get_message(data)


class PageFilter(custom_filters.AdvancedCustomFilter):
    key = "page"

    def check(self, message, pages):
        if type(pages) in [list, tuple]:
            for page in pages:
                if get_data(message.chat.id, "page") == page:
                    return True
            return False
        return get_data(message.chat.id, "page") == pages
