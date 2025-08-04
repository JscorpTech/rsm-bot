from telebot.handler_backends import State, StatesGroup


class RegisterState(StatesGroup):
    full_name = State()
    phone = State()
