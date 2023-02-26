"""Base class for all clients."""
from abc import ABC, abstractmethod


class Client(ABC):
    @abstractmethod
    def __init__(self):
        pass
