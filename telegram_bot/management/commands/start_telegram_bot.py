import os

from django.core.management import BaseCommand

from telegram_bot.services.bot import start_bot


class Command(BaseCommand):
    help = "Start Telegram bot"
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    def handle(self, *args, **options):
        print("start telegram bot")
        start_bot()
