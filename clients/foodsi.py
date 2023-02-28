import json
from typing import List, Dict

import requests

from notifiers.telegram import Telegram
from clients.client import Client
from utils.location import Location

class Foodsi(Client):

    def __init__(self, location: Location, notifier: Telegram, verbose: bool = False):
        self.msg_cache: Dict[str, int] = {}
        self.notifier = notifier
        self.verbose = verbose
        self.location = location

    def _get_item_reqs(self):
        return {
            "distance": {
                "lat": self.location.latitude,
                "lng": self.location.longitude,
                "range": self.location.radius
            },
            "hide_unavailable": True,
        }

    def _get_items(self) -> List[Dict]:
        reqs = self._get_item_reqs()
        resp = requests.post(
            'https://api.foodsi.pl/api/v2/restaurants',
            headers={
                'Content-type':'application/json',
                'system-version':'android_3.0.0',
                'user-agent':'okhttp/3.12.0'},
            data=json.dumps(reqs)
        )
        return resp.json()

    def _process_items(self, items: List[Dict]):
        print(items)
