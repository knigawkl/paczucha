import schedule

from notifiers.telegram import Telegram
from clients.tgtg import TGTG
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

    schedule.every().minute.do(tgtg.scan)
    schedule.every(20).minutes.do(dev_tgtg.scan)

    while True:
        schedule.run_pending()
