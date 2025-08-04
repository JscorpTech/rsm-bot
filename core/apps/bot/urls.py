from django.urls import include, path

from core.apps.bot.views.bot import BotView

urlpatterns = [
    path("webhook/", BotView.as_view(), name="bot"),
]
