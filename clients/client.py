"""Base class for all clients."""
from abc import ABC, abstractmethod

from notifiers.telegram import Telegram


class Client(ABC):

    notifier: Telegram

    @abstractmethod
    def scan(self):
        pass
