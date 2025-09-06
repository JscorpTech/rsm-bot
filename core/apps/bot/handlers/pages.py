import logging

from django.conf import settings
from django.core.files.base import ContentFile
from telebot.types import InputMediaPhoto, InputMediaVideo, Message, ReplyKeyboardRemove

from core.apps.bot import buttons
from core.apps.bot.bot import bot
from core.apps.bot.models import AddressModel, CategoryModel, HotelModel
from core.apps.bot.models.hotel import File, HotelOrder
from core.apps.bot.models.mini_tour import MiniTourOrder, PackageModel
from core.apps.bot.models.transfer import TransferOrder
from core.apps.bot.models.visa import VisaOrder
from core.apps.bot.services import get_data
from core.apps.bot.services import get_message as _
from core.apps.bot.services import get_message_key, get_user, set_data, update_lang
from core.apps.bot.states import HotelState, RegisterState, TransferState
from core.apps.bot.states.pages import MiniTourState, VisaState

from .commands import home


@bot.message_handler(message="back_home")
def back_home(msg: Message):
    set_data(msg.chat.id, "page", "home")
    bot.delete_state(msg.chat.id)
    bot.send_message(msg.chat.id, _("home"), reply_markup=buttons.home())  # type: ignore


@bot.message_handler(message="back")
def back(msg: Message):
    page = get_data(msg.chat.id, "page")
    if page == "hotel":
        state = bot.get_state(msg.chat.id)
        match state:
            case "HotelState:location":
                home(msg)
                return
            case "HotelState:tariff":
                hotel_list_handler(msg)
                return
            case "HotelState:hotel":
                hotel_location_handler(msg, True)
                return
            case (
                "HotelState:hotel_break" | "HotelState:arrival_date" | "HotelState:departure_date" | "HotelState:detail"
            ):
                hotel_tariff_handler(msg, True)
                return

    bot.delete_state(msg.chat.id)
    if page in ["change_lang", "transfer", "mini_tour", "visa", "hotel"]:
        set_data(msg.chat.id, "page", "home")
        bot.send_message(
            msg.chat.id,
            _("home"),
            reply_markup=buttons.home(),
        )
        return

    return back_home(msg)


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
            bot.send_message(msg.chat.id, _("putb"))
            return
        with bot.retrieve_data(msg.chat.id) as data:
            data["hotel_location"] = location.first().pk  # type: ignore
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
                bot.send_message(msg.chat.id, _("putb"))
                return
        else:
            category = CategoryModel.objects.filter(pk=data["hotel_category"])

        data["hotel_category"] = category.first().pk
        hotels = HotelModel.objects.filter(category=category.first(), location__id=data["hotel_location"])
        if not hotels.exists():
            bot.send_message(msg.chat.id, _("no_hotels"))
            return
        bot.set_state(msg.chat.id, HotelState.hotel)
        bot.send_message(
            msg.chat.id,
            category.first().desc % {"location": AddressModel.objects.filter(pk=data["hotel_location"]).first().name},
            reply_markup=buttons.hotel_list(hotels.values_list("name", flat=True)),
        )


@bot.message_handler(state=HotelState.hotel)
def hotel_handler(msg: Message):
    hotels = HotelModel.objects.filter(name=msg.text)
    if not hotels.exists():
        bot.send_message(msg.chat.id, _("putb"))
        return
    with bot.retrieve_data(msg.chat.id) as data:
        hotel = hotels.first()
        data["hotel"] = hotel.pk
        bot.send_message(msg.chat.id, "%s\n%s" % (hotel.name, hotel.desc), reply_markup=buttons.hotel_detail())
        bot.set_state(msg.chat.id, HotelState.detail)


@bot.message_handler(message="videos_images")
def hotel_break_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        files = File.objects.filter(hotel_id=data["hotel"])
        if not files.exists():
            bot.send_message(msg.chat.id, _("video_images_emptry"))
            return
        media = []
        try:
            for file in files:
                file_path = file.file.path
                if file.file_type == "image":
                    if file.file_id is not None:
                        media.append(InputMediaPhoto(file.file_id))
                        continue
                    media.append(InputMediaPhoto(open(file_path, "rb")))
                if file.file_type == "video":
                    if file.file_id is not None:
                        media.append(InputMediaVideo(file.file_id))
                        continue
                    media.append(InputMediaVideo(open(file_path, "rb")))
            res = bot.send_media_group(msg.chat.id, media)
            for tfile, file_instance in zip(res, files):
                if file_instance.file_type == "video":
                    file_instance.file_id = tfile.video.file_id
                if file_instance.file_type == "image":
                    file_instance.file_id = tfile.photo[-1].file_id
                file_instance.save()
        except Exception as e:
            logging.error(str(e))
            print(e)


@bot.message_handler(message="break", state=HotelState.detail)
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

    bot.set_state(msg.chat.id, HotelState.rooms)
    bot.send_message(
        msg.chat.id,
        _("enter_how_many_rooms"),
        reply_markup=buttons.power_type(),
    )


@bot.message_handler(state=HotelState.rooms)
def hotel_rooms_handler(msg: Message):
    if not msg.text.isdigit():
        bot.send_message(msg.chat.id, _("please_enter_number"), reply_markup=buttons.back())
        return
    with bot.retrieve_data(msg.chat.id) as data:
        data["hotel_rooms"] = msg.text
        bot.send_message(
            msg.chat.id,
            _("enter_power_type"),
            reply_markup=buttons.home(),
        )


@bot.message_handler(state=HotelState.power_type)
def hotel_power_type_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["power_type"] = msg.text

    bot.set_state(msg.chat.id, HotelState.transfer)
    bot.send_message(
        msg.chat.id,
        _("enter_transfer"),
        reply_markup=buttons.yes_no(),
    )


@bot.message_handler(state=HotelState.transfer)
def hotel_power_type_handler(msg: Message):
    if (_("yes") != msg.text) and _("no") != msg.text:
        bot.send_message(msg.chat.id, _("putb"))
    with bot.retrieve_data(msg.chat.id) as data:
        data["transfer"] = msg.text == _("yes")

        HotelOrder.objects.create(
            user=get_user(msg.chat.id),
            hotel_id=data["hotel"],
            location_id=data["hotel_location"],
            category_id=data["hotel_category"],
            arrival_date=data["arrival_date"],
            departure_date=data["departure_date"],
            rooms=data["hotel_rooms"],
            transfer=data["transfer"],
            power_type=data["power_type"],
        )
        bot.delete_state(msg.chat.id)
        bot.send_message(
            msg.chat.id,
            _("confirmed_order"),
            reply_markup=buttons.back(),
        )


@bot.message_handler(message="mini_tour")
def mini_tour_handler(msg: Message):
    set_data(msg.chat.id, "page", "mini_tour")
    bot.set_state(msg.chat.id, MiniTourState.location)
    bot.send_message(
        msg.chat.id,
        _("mini_tour"),
        reply_markup=buttons.mini_tour(),
    )


@bot.message_handler(state=MiniTourState.location)
def mini_tour_category_handler(msg: Message):
    category = AddressModel.objects.filter(name=msg.text, service="mini_tour")
    if not category.exists():
        bot.send_message(msg.chat.id, _("putb"))
        return
    with bot.retrieve_data(msg.chat.id) as data:
        data["location"] = category.first().id
        bot.set_state(msg.chat.id, MiniTourState.package)
        bot.send_message(msg.chat.id, _("enter_package"), reply_markup=buttons.mini_tour_packages())


@bot.message_handler(state=MiniTourState.package)
def mini_tour_package_handler(msg: Message):
    package = PackageModel.objects.filter(name=msg.text)
    if not package.exists():
        bot.send_message(msg.chat.id, _("putb"))
        return
    with bot.retrieve_data(msg.chat.id) as data:
        package = package.first()
        data["package"] = package.id
        bot.set_state(msg.chat.id, MiniTourState.detail)
        with open(package.file.path, "rb") as file:
            bot.send_document(msg.chat.id, file, caption=package.desc, reply_markup=buttons.mini_tour_detail())


@bot.message_handler(message="break", state=MiniTourState.detail)
def mini_tour_break(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        MiniTourOrder.objects.create(
            user=get_user(msg.chat.id),
            address_id=data["location"],
            package_id=data["package"],
        )
        bot.send_message(msg.chat.id, _("confirmed_order"), reply_markup=buttons.home())
        bot.delete_state(msg.chat.id)
        set_data(msg.chat.id, "page", "home")


@bot.message_handler(message="transfer")
def transfer_handler(msg: Message):
    set_data(msg.chat.id, "page", "transfer")
    bot.send_message(
        msg.chat.id,
        _("transfer_desc"),
        reply_markup=buttons.transfer(),
    )
    bot.set_state(msg.chat.id, TransferState.service_type)


@bot.message_handler(state=TransferState.service_type, message=settings.TRANSFER_SERVICE_TYPES)
def transfer_service_type_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["transfer_service_type"] = msg.text
        bot.send_message(msg.chat.id, _("enter_transfer_category"), reply_markup=buttons.transfer_category())
        bot.set_state(msg.chat.id, TransferState.category)


@bot.message_handler(state=TransferState.category)
def transfer_category_handler(msg: Message):
    category = CategoryModel.objects.filter(name=msg.text)
    if not category.exists():
        bot.send_message(msg.chat.id, _("putb"))
        return
    with bot.retrieve_data(msg.chat.id) as data:
        data["transfer_category"] = category.first().id
        bot.send_message(msg.chat.id, _("enter_transfer_date"), reply_markup=buttons.back())
        bot.set_state(msg.chat.id, TransferState.transfer_date)


@bot.message_handler(state=TransferState.transfer_date)
def transfer_date_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["transfer_date"] = msg.text
        bot.send_message(msg.chat.id, _("enter_passanger_count"), reply_markup=buttons.back())
        bot.set_state(msg.chat.id, TransferState.passanger_count)


@bot.message_handler(state=TransferState.passanger_count)
def transfer_date_handler(msg: Message):
    if not msg.text.isdigit():
        bot.send_message(msg.chat.id, _("please_enter_number"))
        return
    with bot.retrieve_data(msg.chat.id) as data:
        data["transfer_passanger_count"] = msg.text
        bot.send_message(msg.chat.id, _("enter_goods"), reply_markup=buttons.back())
        bot.set_state(msg.chat.id, TransferState.goods)


@bot.message_handler(state=TransferState.goods)
def transfer_goods_handler(msg: Message):
    if not msg.text.isdigit():
        bot.send_message(msg.chat.id, _("please_enter_number"))
        return
    with bot.retrieve_data(msg.chat.id) as data:
        data["transfer_goods"] = msg.text
        TransferOrder.objects.create(
            user=get_user(msg.chat.id),
            service_type=data["transfer_service_type"],
            category_id=data["transfer_category"],
            date=data["transfer_date"],
            passanger_count=data["transfer_passanger_count"],
            goods=data["transfer_goods"],
        )
        bot.send_message(msg.chat.id, _("confirmed_order"), reply_markup=buttons.home())
        bot.delete_state(msg.chat.id)


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
        bot.send_message(msg.chat.id, _("enter_first_name"), reply_markup=ReplyKeyboardRemove())
        return
    bot.send_message(
        msg.chat.id,
        _("home"),
        reply_markup=buttons.home(),
    )


@bot.message_handler(message="visa")
def visa_handler(msg: Message):
    set_data(msg.chat.id, "page", "visa")
    bot.send_message(msg.chat.id, _("select_visa_type"), reply_markup=buttons.visa())
    bot.set_state(msg.chat.id, VisaState.service_type)


@bot.message_handler(message=settings.VISA_SERVICE_TYPES, state=VisaState.service_type)
def visa_service_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["visa_service"] = msg.text
    bot.send_message(msg.chat.id, _("enter_full_name"), reply_markup=buttons.back())
    bot.set_state(msg.chat.id, VisaState.full_name)


@bot.message_handler(state=VisaState.full_name)
def visa_full_name_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["full_name"] = msg.text
    bot.send_message(msg.chat.id, _("enter_birth_date"), reply_markup=buttons.back())
    bot.set_state(msg.chat.id, VisaState.birth_date)


@bot.message_handler(state=VisaState.birth_date)
def visa_full_name_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["birth_date"] = msg.text
    bot.send_message(msg.chat.id, _("enter_nationaliry"), reply_markup=buttons.back())
    bot.set_state(msg.chat.id, VisaState.nationality)


@bot.message_handler(state=VisaState.nationality)
def visa_nationality_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["nationality"] = msg.text
    bot.send_message(msg.chat.id, _("enter_passport_front"), reply_markup=buttons.back())
    bot.set_state(msg.chat.id, VisaState.passport_front)


@bot.message_handler(state=VisaState.passport_front, content_types=["photo"])
def visa_passport_front_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["passport_front"] = msg.photo[-1].file_id
    bot.send_message(msg.chat.id, _("enter_passport_back"), reply_markup=buttons.back())
    bot.set_state(msg.chat.id, VisaState.passport_back)


@bot.message_handler(state=VisaState.passport_back, content_types=["photo"])
def visa_passport_back_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        data["passport_back"] = msg.photo[-1].file_id
    bot.send_message(msg.chat.id, _("enter_planned_date"), reply_markup=buttons.back())
    bot.set_state(msg.chat.id, VisaState.date)


@bot.message_handler(state=VisaState.date)
def visa_date_handler(msg: Message):
    with bot.retrieve_data(msg.chat.id) as data:
        try:
            data["date"] = msg.text
            passport_front = bot.download_file(bot.get_file(data["passport_front"]).file_path)
            passport_back = bot.download_file(bot.get_file(data["passport_back"]).file_path)
            VisaOrder.objects.create(
                user=get_user(msg.chat.id),
                passport_front=ContentFile(passport_front, name=data["passport_front"] + ".jpg"),
                passport_back=ContentFile(passport_back, name=data["passport_back"] + ".jpg"),
                full_name=data["full_name"],
                birth_date=data["birth_date"],
                nationality=data["nationality"],
                passport_front_file_id=data["passport_front"],
                passport_back_file_id=data["passport_back"],
                date=data["date"],
                service=data["visa_service"],
            )
            bot.send_message(msg.chat.id, _("confirmed_order"), reply_markup=buttons.home())
            bot.delete_state(msg.chat.id)
        except Exception as e:
            print(e)


@bot.message_handler(message="contact")
def contact_handler(msg: Message):
    bot.send_message(msg.chat.id, _("contact_desc"))
