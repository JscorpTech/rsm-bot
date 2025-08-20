import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from config.env import env
from core.apps.bot.bot import bot
from core.apps.bot.models import HotelOrder, TransferOrder, VisaOrder
from core.apps.bot.models.mini_tour import MiniTourOrder
from core.apps.bot.services import get_message as _


@receiver(post_save, sender=HotelOrder)
def HotelOrderSignal(sender, instance, created, **kwargs):
    try:
        message = _("hotel_order_detail") % {
            "full_name": instance.user.full_name,
            "phone": instance.user.phone,
            "arrival_data": instance.arrival_date,
            "departure_data": instance.departure_date,
            "rooms": instance.rooms,
            "hotel": instance.hotel.name,
            "transfer": instance.transfer,
            "power_type": instance.power_type,
            "status": instance.status,
            "category": instance.category.name,
            "location": instance.location.name,
            "link": env.str("DOMAIN") + reverse("admin:bot_hotelorder_change", args=[instance.id]),
        }
        bot.send_message(env.str("CHANNEL"), message)
    except Exception as e:
        logging.error(str(e))


@receiver(post_save, sender=TransferOrder)
def TransferOrderSignal(sender, instance, created, **kwargs):
    try:
        message = _("transfer_order_detail") % {
            "service_type": instance.service_type,
            "category": instance.category.name,
            "passanger_count": instance.passanger_count,
            "date": instance.date,
            "goods": instance.goods,
            "status": instance.status,
            "link": env.str("DOMAIN") + reverse("admin:bot_transferorder_change", args=[instance.id]),
        }
        bot.send_message(env.str("CHANNEL"), message)
    except Exception as e:
        logging.error(str(e))


@receiver(post_save, sender=VisaOrder)
def VisaOrderSignal(sender, instance, created, **kwargs):
    try:
        message = _("transfer_order_detail") % {
            "full_name": instance.full_name,
            "date": instance.date,
            "nationality": instance.nationality,
            "birth_date": instance.birth_date,
            "service": instance.service,
            "status": instance.status,
            "link": env.str("DOMAIN") + reverse("admin:bot_visaorder_change", args=[instance.id]),
        }
        bot.send_message(env.str("CHANNEL"), message)
    except Exception as e:
        logging.error(str(e))


@receiver(post_save, sender=MiniTourOrder)
def MiniTourOrderSignal(sender, instance, created, **kwargs):
    try:
        message = _("mini_tour_order_detail") % {
            "full_name": instance.full_name,
            "phone": instance.user.phone,
            "package": instance.package.name,
            "location": instance.address.name,
            "status": instance.status,
            "link": env.str("DOMAIN") + reverse("admin:bot_visaorder_change", args=[instance.id]),
        }
        bot.send_message(env.str("CHANNEL"), message)
    except Exception as e:
        logging.error(str(e))
