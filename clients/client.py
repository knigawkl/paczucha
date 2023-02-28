"""Base class for all clients."""
from abc import ABC, abstractmethod
from typing import List, Dict

from notifiers.telegram import Telegram


class Client(ABC):

    msg_cache: Dict[str, int]
    notifier: Telegram
    verbose: bool = False

    def __del__(self):
        for msg_id in self.msg_cache.values():
            self.notifier.delete(msg_id)

    @abstractmethod
    def _get_items(self) -> List[Dict]:
        pass

    @staticmethod
    @abstractmethod
    def _get_item_id(item: Dict):
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
            item_id = self._get_item_id(item)
            self._del_msg(item_id)
            count = self._get_count(item)
            if not count and not self.verbose:
                continue
            name = self._get_name(item)
            pickup_interval = self._get_pickup_interval(item)
            msg = self._form_msg(name, count, pickup_interval)
            msg_id = self.notifier.notify(msg)
            self.msg_cache[item_id] = msg_id

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
