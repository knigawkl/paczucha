from typing import List, Dict, Optional

from tgtg import TgtgClient

from clients.client import Client
from notifiers.notifier import Notifier
from utils.location import Location


class TGTG(Client, TgtgClient):

    def __init__(self, access_token: str, refresh_token: str, user_id: str, cookie: str,
                 notifiers: List[Notifier], location: Optional[Location] = None):
        self.tgtg = TgtgClient(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            cookie=cookie
        )
        self.location = location
        self.notifiers = notifiers

    def get_items(self) -> Optional[List[Dict]]:
        try:
            return self.tgtg.get_items(favorites_only=True)
        except Exception as e:
            return None

    def process_items(self, items: Optional[List[Dict]]):
        for item in items:
            items_available = item.get('items_available')
            # if not items_available:
            #     continue
            display_name = item.get('display_name')
            msg = f'{display_name}: {items_available}'
            self.notify(msg.replace('&', 'i'))

    def scan(self, package_names: Optional[List[str]] = None):
        items = self.get_items()
        self.process_items(items)
