"""Base class for all clients."""
from abc import ABC, abstractmethod
from typing import List, Dict

from notifiers.telegram import Telegram


class Client(ABC):
    """Base class for all clients."""

    TIMEOUT = 5
    msg_ids: List[int] = []
    notifier: Telegram
    verbose: bool = False

    def __del__(self):
        self._del_msgs()

    def _del_msgs(self):
        """Delete sent notifications."""
        for msg_id in self.msg_ids:
            self.notifier.delete(msg_id)
        self.msg_ids = []

    @abstractmethod
    def _get_items(self) -> List[Dict]:
        pass

    @staticmethod
    @abstractmethod
    def _get_count(item: Dict):
        pass

    @staticmethod
    @abstractmethod
    def _get_name(item: Dict):
        pass

    @staticmethod
    @abstractmethod
    def _get_pickup_interval(item: Dict):
        pass

    def _process_items(self, items: List[Dict]):
        for item in items:
            count = self._get_count(item)
            if not count and not self.verbose:
                continue
            name = self._get_name(item)
            pickup_interval = self._get_pickup_interval(item)
            msg = self._form_msg(name, count, pickup_interval)
            msg_id = self.notifier.notify(msg)
            if msg_id:
                self.msg_ids.append(msg_id)

    @classmethod
    def _form_msg(cls, display_name: str, items_available: int, pickup_interval: str):
        return f'{display_name}\n' \
               f'Available: {items_available}\n' \
               f'Pickup time: {pickup_interval}\n' \
               f'Source: {cls.__name__}'

    def scan(self):
        """Look for items of interest."""
        self._del_msgs()
        items = self._get_items()
        self._process_items(items)
