from telebot.types import Message

from core.apps.bot import buttons
from core.apps.bot.bot import bot
from core.apps.bot.models import AddressModel, CategoryModel, HotelModel
from core.apps.bot.services import get_data
from core.apps.bot.services import get_message as _
from core.apps.bot.services import get_message_key, get_user, set_data, update_lang
from core.apps.bot.states import HotelState, RegisterState

from .commands import home


@bot.message_handler(message="back_home")
def back_home(msg: Message):
    set_data(msg.chat.id, "page", "home")
    bot.delete_state(msg.chat.id)
    bot.send_message(msg.chat.id, _("home"), reply_markup=buttons.home())


@bot.message_handler(message="back")
def back(msg: Message):
    page = get_data(msg.chat.id, "page")
    if page in ["change_lang", "transfer", "mini_tour"]:
        set_data(msg.chat.id, "page", "home")
        bot.send_message(
            msg.chat.id,
            _("home"),
            reply_markup=buttons.home(),
        )
    if page == "hotel":
        state = bot.get_state(msg.chat.id)
        match state:
            case "HotelState:location":
                home(msg)
            case "HotelState:tariff":
                hotel_list_handler(msg)
            case "HotelState:hotel":
                hotel_location_handler(msg, True)
            case "HotelState:hotel_break" | "HotelState:arrival_date" | "HotelState:departure_date":
                hotel_tariff_handler(msg, True)


@bot.message_handler(message="hotel")
def hotel_list_handler(msg: Message):
    set_data(msg.chat.id, "page", "hotel")
    bot.set_state(msg.chat.id, HotelState.location)
    bot.send_message(
        msg.chat.id,
        _("hotel"),
        reply_markup=buttons.hotel_locations(),
    )


@bot.message_handler(state=HotelState.location)
def hotel_location_handler(msg: Message, is_back=False):
    if not is_back:
        location = AddressModel.objects.filter(name=msg.text)
        if not location.exists():
            bot.send_message(msg.chat.id, _("please_use_the_buttons"))
            return
        with bot.retrieve_data(msg.chat.id) as data:
            data["hotel_location"] = location.first().pk
    bot.set_state(msg.chat.id, HotelState.tariff)
    bot.send_message(
        msg.chat.id,
        _("select_hotel_tariff"),
        reply_markup=buttons.hotel_tariff(),
    )


@bot.message_handler(state=HotelState.tariff)
def hotel_tariff_handler(msg: Message, is_back=False):
    with bot.retrieve_data(msg.chat.id) as data:
        if not is_back:
            category = CategoryModel.objects.filter(name=msg.text)
            if not category.exists():
                bot.send_message(msg.chat.id, _("please_use_the_buttons"))
                return
        else:
            category = CategoryModel.objects.filter(pk=data["hotel_category"])

        data["hotel_category"] = category.first().pk
        hotels = HotelModel.objects.filter(category=category.first(),
                                           location__id=data["hotel_location"])
        if not hotels.exists():
            bot.send_message(msg.chat.id, _("no_hotels"))
            return
        bot.set_state(msg.chat.id, HotelState.hotel)
        bot.send_message(
            msg.chat.id,
            _("select_hotel"),
            reply_markup=buttons.hotel_list(
                hotels.values_list("name", flat=True)),
        )


@bot.message_handler(state=HotelState.hotel)
def hotel_handler(msg: Message):
    hotels = HotelModel.objects.filter(name=msg.text)
    if not hotels.exists():
        bot.send_message(msg.chat.id, _("please_use_the_buttons"))
        return
    with bot.retrieve_data(msg.chat.id) as data:
        hotel = hotels.first()
        data["hotel"] = hotel.pk
        bot.send_message(msg.chat.id,
                         "%s\n%s" % (hotel.name, hotel.desc),
                         reply_markup=buttons.hotel_break())
        bot.set_state(msg.chat.id, HotelState.hotel_break)


@bot.message_handler(state=HotelState.hotel_break)
def hotel_break_handler(msg: Message):
    bot.set_state(msg.chat.id, HotelState.arrival_date)
    bot.send_message(
        msg.chat.id,
        _("enter_arrival_date"),
        reply_markup=buttons.back(),
    )


@bot.message_handler(state=HotelState.arrival_date)
def hotel_arrival_date_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["arrival_date"] = msg.text
    bot.set_state(msg.chat.id, HotelState.departure_date)
    bot.send_message(
        msg.chat.id,
        _("enter_departure_date"),
        reply_markup=buttons.back(),
    )


@bot.message_handler(state=HotelState.departure_date)
def hotel_departure_date_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["departure_date"] = msg.text

    bot.set_state(msg.chat.id, HotelState.departure_date)
    bot.send_message(
        msg.chat.id,
        _("enter_departure_date"),
        reply_markup=buttons.back(),
    )


@bot.message_handler(message="mini_tour")
def mini_tour_handler(msg: Message):
    set_data(msg.chat.id, "page", "mini_tour")
    bot.send_message(
        msg.chat.id,
        _("mini_tour"),
        reply_markup=buttons.mini_tour(),
    )


# @bot.message_handler(state=HotelState.tariff, messages=settings.HOTEL_TARIFF)
@bot.message_handler(message="transfer")
def transfer_handler(msg: Message):
    set_data(msg.chat.id, "page", "transfer")
    bot.send_message(
        msg.chat.id,
        _("transfer_desc"),
        reply_markup=buttons.transfer(),
    )


@bot.message_handler(message="change_lang")
def change_lang(msg: Message):
    set_data(msg.chat.id, "page", "change_lang")
    bot.send_message(
        msg.chat.id,
        _("select_lang"),
        reply_markup=buttons.lang(),
    )


@bot.message_handler(message=["uz", "en", "ru"])
def select_lang(msg: Message):
    set_data(msg.chat.id, "page", "home")
    update_lang(msg.chat.id, get_message_key(msg.text, "uz"))
    user = get_user(msg.chat.id)
    if not user.is_register:
        set_data(msg.chat.id, "page", "register")
        bot.set_state(msg.from_user.id, RegisterState.full_name, msg.chat.id)
        bot.send_message(msg.chat.id, _("enter_first_name"))
        return
    bot.send_message(
        msg.chat.id,
        _("home"),
        reply_markup=buttons.home(),
    )


@bot.message_handler(message="contact")
def contact_handler(msg: Message):
    bot.send_message(msg.chat.id, _("contact_desc"))
