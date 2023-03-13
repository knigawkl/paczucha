import pytest

from clients.tgtg import TGTG, TGTGConfig
from notifiers.telegram import Telegram
from config import settings


@pytest.fixture
def tgtg_item():
    yield tgtg_item


@pytest.fixture
def tele():
    yield Telegram(
        token=settings.telegram_token,
        chat_id=settings.telegram.dev_chat_id
    )


@pytest.fixture
def tgtg_client(tele):
    config = TGTGConfig(
        access_token=settings.tgtg.access_token,
        refresh_token=settings.tgtg.refresh_token,
        user_id=settings.tgtg.user_id,
        cookie=settings.tgtg.cookie
    )
    yield TGTG(
        config=config,
        notifier=tele,
        verbose=True
    )


@pytest.fixture
def tgtg_item():
    yield {'item': {'item_id': '470479', 'name': 'Paczka Warzywa & Owoce - Rano'},
        'display_name': 'Biedronka  - Warszawa Kochanowskiego 45/47 (Paczka Warzywa & Owoce - Rano)',
        'pickup_interval': {'start': '2023-03-14T08:00:00Z', 'end': '2023-03-14T10:00:00Z'},
        'items_available': 0}
