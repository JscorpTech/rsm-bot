from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

PAGES = [
    {
        "seperator": False,
        "items": [
            {
                "title": _("Home page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": _("Auth"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Users"),
                "icon": "group",
                "link": reverse_lazy("admin:accounts_user_changelist"),
            },
            {
                "title": _("Group"),
                "icon": "group",
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
        ],
    },
    {
        "title": _("Dashboard"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Manzillar"),
                "icon": "add_location",
                "link": reverse_lazy("admin:bot_addressmodel_changelist"),
            },
            {
                "title": _("Category"),
                "icon": "category",
                "link": reverse_lazy("admin:bot_categorymodel_changelist"),
            },
            {
                "title": _("Paketlar"),
                "icon": "package_2",
                "link": reverse_lazy("admin:bot_packagemodel_changelist"),
            },
            {
                "title": _("Bot foydalanuvchilari"),
                "icon": "groups",
                "link": reverse_lazy("admin:bot_botuser_changelist"),
            },
            {
                "title": _("Tarjimalar"),
                "icon": "translate",
                "link": reverse_lazy("admin:bot_messages_changelist"),
            },
            {
                "title": _("Mexmonxonalar"),
                "icon": "hotel",
                "link": reverse_lazy("admin:bot_hotelmodel_changelist"),
            },
        ],
    },
    {
        "title": _("Buyurtmalar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Mexmonxona buyurtmalar"),
                "icon": "hotel",
                "link": reverse_lazy("admin:bot_hotelorder_changelist"),
            },
            {
                "title": _("visa buyurtmalar"),
                "icon": "card_membership",
                "link": reverse_lazy("admin:bot_visaorder_changelist"),
            },
            {
                "title": _("Transfer buyurtmalar"),
                "icon": "airport_shuttle",
                "link": reverse_lazy("admin:bot_transferorder_changelist"),
            },
            {
                "title": _("Mini Tour buyurtmalar"),
                "icon": "festival",
                "link": reverse_lazy("admin:bot_minitourorder_changelist"),
            },
        ],
    },
]
