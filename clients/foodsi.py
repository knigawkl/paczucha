import json
from typing import List, Dict
from datetime import datetime

import requests

from notifiers.telegram import Telegram
from clients.client import Client
from utils.location import Location

class Foodsi(Client):

    def __init__(self, location: Location, notifier: Telegram, verbose: bool = False, package_names: List[str] = []):
        self.msg_cache: Dict[str, int] = {}
        self.notifier = notifier
        self.verbose = verbose
        self.location = location
        self.package_names = package_names

    @staticmethod
    def _get_id(item: Dict):
        return item.get('id')

    @staticmethod
    def _get_count(item: Dict):
        return item.get('meals_amount', 0)

    @staticmethod
    def _get_name(item: Dict):
        return item.get('name')

    @staticmethod
    def _get_pickup_interval(item: Dict):
        for_day = item.get('for_day')
        for_day = datetime.strptime(for_day, '%Y-%m-%d')
        day = for_day.strftime('%d.%m')

        extended_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        collection_day = item.get('package_day', {}).get('collection_day', {})
        start, end = collection_day.get('opened_at'), collection_day.get('closed_at')
        start, end = datetime.strptime(start, extended_format), datetime.strptime(end, extended_format)

        time_start = start.strftime('%H:%M')
        time_end = end.strftime('%H:%M')
        return f'{day} {time_start}-{time_end}'

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
        data = resp.json().get('data')
        return [item for item in data if self._get_name(item) in self.package_names]
