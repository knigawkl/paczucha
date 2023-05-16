"""Cron dev version."""
from notifiers.telegram import Telegram
from clients.tgtg import TGTG, TGTGConfig
from clients.foodsi import Foodsi
from utils.location import Location
from config import settings


if __name__ == '__main__':
    location = Location(**settings.location)
    dev_tele = Telegram(
        token=settings.telegram_token,
        chat_id=settings.telegram.dev_chat_id
    )
    tgtg_config = TGTGConfig(
        access_token=settings.tgtg.access_token,
        refresh_token=settings.tgtg.refresh_token,
        user_id=settings.tgtg.user_id,
        cookie=settings.tgtg.cookie
    )
    dev_tgtg = TGTG(
        config=tgtg_config,
        notifier=dev_tele,
        verbose=True
    )
    dev_foodsi = Foodsi(
        location=location,
        notifier=dev_tele,
        verbose=True,
        package_names=['Sushi Fudżi', 'Circle K Conrada']
    )

    # dev_tgtg.scan()
    dev_foodsi.scan()
