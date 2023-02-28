from typing import List, Dict

from notifiers.telegram import Telegram
from clients.client import Client
from utils.location import Location

class Foodsi(Client):

    def __init__(self, location: Location, notifier: Telegram, verbose: bool = False):
        self.msg_cache: Dict[str, int] = {}
        self.notifier = notifier
        self.verbose = verbose

    def _get_items(self) -> List[Dict]:
        pass

    def _process_items(self, items: List[Dict]):
        pass
