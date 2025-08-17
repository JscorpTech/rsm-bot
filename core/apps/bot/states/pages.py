from telebot.handler_backends import State, StatesGroup


class HotelState(StatesGroup):
    location = State()
    tariff = State()
    hotel = State()
    hotel_break = State()
    arrival_date = State()
    departure_date = State()
    rooms = State()
    detail = State()


class TransferState(StatesGroup):
    service_type = State()
    category = State()
    transfer_date = State()
    passanger_count = State()
    goods = State()


class VisaState(StatesGroup):
    service_type = State()
    full_name = State()
    birth_date = State()
    nationality = State()
    passport_front = State()
    passport_back = State()
    date = State()


class AdminState(StatesGroup):
    file_id = State()
