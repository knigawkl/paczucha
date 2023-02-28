"""Base class for all clients."""
from abc import ABC, abstractmethod
from typing import List, Dict

from notifiers.telegram import Telegram


class Client(ABC):

    msg_cache: Dict[str, int]
    notifier: Telegram

    def __del__(self):
        for msg_id in self.msg_cache.values():
            self.notifier.delete(msg_id)

    @abstractmethod
    def _get_items(self) -> List[Dict]:
        pass

    @abstractmethod
    def _process_items(self, items: List[Dict]):
        pass

    @classmethod
    def _form_msg(cls, display_name: str, items_available: int, pickup_interval: str):
        return f'{display_name}\n' \
               f'Available: {items_available}\n' \
               f'Pickup time: {pickup_interval}\n' \
               f'Source: {cls.__name__}'

    def _del_msg(self, item_id):
        if item_id in self.msg_cache:
            msg_id = self.msg_cache.get(item_id)
            self.notifier.delete(msg_id)
            self.msg_cache.pop(item_id)

    def scan(self):
        items = self._get_items()
        self._process_items(items)
