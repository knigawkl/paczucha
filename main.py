import schedule

from notifiers.telegram import Telegram
from clients.tgtg import TGTG
from clients.foodsi import Foodsi
from config import settings


if __name__ == '__main__':
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
        notifiers=[tele]
    )
    # foodsi = Foodsi(
    #     notifiers=[tele]
    # )

    schedule.every().minute.do(tgtg.scan)
    schedule.every().hour.do(dev_tele.notify, msg='I am alive.')

    while True:
        schedule.run_pending()
