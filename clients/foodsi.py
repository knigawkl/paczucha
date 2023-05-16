"""This module contains the Foodsi class."""
import json
from typing import List, Dict, Tuple
from datetime import datetime

import requests

from notifiers.telegram import Telegram
from clients.client import Client
from utils.location import Location

class Foodsi(Client):  # pylint: disable=too-few-public-methods
    """The foodsi.pl client."""

    def __init__(self, location: Location, notifier: Telegram, verbose: bool = False,
                 package_names: List[str] = None):
        self.notifier = notifier
        self.verbose = verbose
        self.location = location
        self.package_names = package_names

    @staticmethod
    def _get_count(item: Dict):
        return item.get('package_day', {}).get('meals_left', '?')

    @staticmethod
    def _get_name(item: Dict):
        return item.get('name')

    def _get_pickup_interval(self, item: Dict):
        collection_day = item.get('package_day', {}).get('collection_day', {})
        weekday = self._get_weekday(collection_day)
        time_start, time_end = self._get_timeframe(collection_day)

        return f'{weekday} {time_start}-{time_end}'

    @staticmethod
    def _get_weekday(collection_day: Dict) -> str:
        weekday_int = collection_day.get('week_day', 8)
        weekday_mapping = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday',
            8: ''
        }
        return weekday_mapping.get(weekday_int)

    @staticmethod
    def _get_timeframe(collection_day: Dict) -> Tuple[str, str]:
        extended_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        start, end = collection_day.get('opened_at'), collection_day.get('closed_at')
        start = datetime.strptime(start, extended_format)
        end = datetime.strptime(end, extended_format)
        time_start = start.strftime('%H:%M')
        time_end = end.strftime('%H:%M')
        return time_start, time_end

    def _get_item_reqs(self):
        return {
            "distance": {
                "lat": self.location.latitude,
                "lng": self.location.longitude,
                "range": self.location.radius
            },
            "hide_unavailable": not self.verbose,
        }

    def _get_items(self) -> List[Dict]:
        reqs = self._get_item_reqs()
        resp = requests.post(
            'https://api.foodsi.pl/api/v2/restaurants',
            headers={
                'Content-type':'application/json',
                'system-version':'android_3.0.0',
                'user-agent':'okhttp/3.12.0'},
            data=json.dumps(reqs),
            timeout=Client.TIMEOUT
        )
        data = resp.json().get('data')
        return [item for item in data if self._get_name(item) in self.package_names]
