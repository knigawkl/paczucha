"""Base class for all notifiers."""
from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    def notify(self, msg: str):
        pass
