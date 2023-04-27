"""Cron version."""
from notifiers.telegram import Telegram
from clients.tgtg import TGTG, TGTGConfig
from clients.foodsi import Foodsi
from utils.location import Location
from config import settings


if __name__ == '__main__':
    location = Location(**settings.location)
    tele = Telegram(
        token=settings.telegram_token,
        chat_id=settings.telegram.chat_id
    )
    tgtg_config = TGTGConfig(
        access_token=settings.tgtg.access_token,
        refresh_token=settings.tgtg.refresh_token,
        user_id=settings.tgtg.user_id,
        cookie=settings.tgtg.cookie
    )
    tgtg = TGTG(
        config=tgtg_config,
        notifier=tele
    )
    foodsi = Foodsi(
        location=location,
        notifier=tele,
        package_names=settings.package_names
    )

    tgtg.scan()
    foodsi.scan()
