import schedule

from notifiers.telegram import Telegram
from clients.tgtg import TGTG
from clients.foodsi import Foodsi
from utils.location import Location
from config import settings


if __name__ == '__main__':
    location = Location(**settings.location)
    tele = Telegram(
        token=settings.telegram_token,
        chat_id=settings.telegram.chat_id
    )
    dev_tele = Telegram(
        token=settings.telegram_token,
        chat_id=settings.telegram.dev_chat_id
    )
    tgtg = TGTG(
        access_token=settings.tgtg.access_token,
        refresh_token=settings.tgtg.refresh_token,
        user_id=settings.tgtg.user_id,
        cookie=settings.tgtg.cookie,
        notifier=tele
    )
    dev_tgtg = TGTG(
        access_token=settings.tgtg.access_token,
        refresh_token=settings.tgtg.refresh_token,
        user_id=settings.tgtg.user_id,
        cookie=settings.tgtg.cookie,
        notifier=dev_tele,
        verbose=True
    )
    foodsi = Foodsi(
        location=location,
        notifier=tele,
        package_names=settings.package_names
    )
    dev_foodsi = Foodsi(
        location=location,
        notifier=dev_tele,
        verbose=True,
        package_names=['Sushi Fudżi', 'Circle K Conrada']
    )

    schedule.every().minute.do(tgtg.scan)
    schedule.every().minute.do(foodsi.scan)
    schedule.every(10).minutes.do(dev_tgtg.scan)
    schedule.every(10).minutes.do(dev_foodsi.scan)

    while True:
        schedule.run_pending()
