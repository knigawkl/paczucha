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

    def _process_items(self, items: List[Dict]):
        for item in items:
            item_id = item.get('item', {}).get('item_id')
            self._del_msg(item_id)
            items_available = item.get('items_available')
            if not items_available and not self.verbose:
                continue
            display_name = item.get('display_name').replace('&', 'i')
            pickup_interval = self._format_pickup_interval(item.get('pickup_interval'))
            msg = self._form_msg(display_name, items_available, pickup_interval)
            msg_id = self.notifier.notify(msg)
            self.msg_cache[item_id] = msg_id

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
