"""Base class for all clients."""
from abc import ABC, abstractmethod
from typing import List, Optional

from notifiers.notifier import Notifier


class Client(ABC):

    notifiers: List[Notifier]

    @abstractmethod
    def scan(self, package_names: Optional[List[str]] = None):
        pass

    def notify(self, msg: str):
        """"""
        for n in self.notifiers:
            n.notify(msg)
