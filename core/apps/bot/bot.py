import logging

from telebot import TeleBot, custom_filters
from telebot.storage.redis_storage import StateRedisStorage

from config.env import env

try:
    storage = StateRedisStorage(redis_url=env.str("REDIS_URL"))
    bot = TeleBot(token=env.str("BOT_TOKEN"), state_storage=storage)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
except Exception as e:
    logging.error("Bot variable yaratilmadi")
    logging.error(e)
