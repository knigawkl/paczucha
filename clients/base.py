"""Base class for all clients."""
from abc import ABC, abstractmethod
from typing import Dict


class Client(ABC):
    @abstractmethod
    def __init__(self, config: Dict):
        pass
