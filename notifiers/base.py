"""Base class for all notifiers."""
from abc import ABC, abstractmethod
from typing import Dict


class Notifier(ABC):

    @abstractmethod
    def __init__(self, config: Dict):
        pass

    @abstractmethod
    def notify(self, msg: str = ''):
        pass
