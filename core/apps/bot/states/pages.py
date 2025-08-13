from telebot.handler_backends import State, StatesGroup


class HotelState(StatesGroup):
    location = State()
    tariff = State()
    hotel = State()
    hotel_break = State()
    arrival_date = State()
    departure_date = State()
