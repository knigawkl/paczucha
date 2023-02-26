"""Telegram client."""

from notifiers.base import Notifier

import requests


class Telegram(Notifier):
    def __init__(self, token: str, chat_id: int) -> None:
        """

        Args:
             token:
             chat_id:

        """
        self.token = token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text="

    def notify(self, msg: str) -> None:
        requests.get(self.url + msg)
