from notifiers.telegram import Telegram
from clients.tgtg import TGTG
from clients.foodsi import Foodsi
from config import settings


if __name__ == '__main__':
    tele = Telegram(
        token=settings.telegram_token,
        chat_id=settings.telegram.chat_id
    )

    TGTG()
    Foodsi()
    tele.notify(msg='test')
