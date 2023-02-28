from typing import List, Dict
from datetime import datetime

from tgtg import TgtgClient

from clients.client import Client
from notifiers.telegram import Telegram
from utils.utils import shift_timezone


class TGTG(Client, TgtgClient):

    def __init__(self, access_token: str, refresh_token: str, user_id: str, cookie: str, notifier: Telegram,
                 verbose: bool = False):
        self.tgtg = TgtgClient(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            cookie=cookie
        )
        self.msg_cache: Dict[str, int] = {}
        self.notifier = notifier
        self.verbose = verbose

    def _get_items(self) -> List[Dict]:
        try:
            return self.tgtg.get_items(favorites_only=True)
        except Exception as e:
            return []

    @staticmethod
    def _get_id(item: Dict) -> str:
        return item.get('item', {}).get('item_id')

    @staticmethod
    def _get_count(item: Dict) -> int:
        return item.get('items_available')

    @staticmethod
    def _get_name(item: Dict) -> str:
        return item.get('display_name').replace('&', 'i')

    @staticmethod
    def _get_pickup_interval(item: Dict):
        return TGTG._format_pickup_interval(item.get('pickup_interval'))

    @staticmethod
    def _format_pickup_interval(pickup_interval: Dict[str, str]):
        iso_format = '%Y-%m-%dT%H:%M:%SZ'
        start, end = pickup_interval.get('start'), pickup_interval.get('end')
        start, end = datetime.strptime(start, iso_format), datetime.strptime(end, iso_format)
        start, end = shift_timezone(start), shift_timezone(end)
        day = start.strftime('%d.%m')
        time_start = start.strftime('%H:%M')
        time_end = end.strftime('%H:%M')
        return f'{day} {time_start}-{time_end}'
