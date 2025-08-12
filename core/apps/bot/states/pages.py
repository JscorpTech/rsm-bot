from telebot.handler_backends import State, StatesGroup


class HotelState(StatesGroup):
    location = State()
    tariff = State()
