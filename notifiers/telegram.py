"""Telegram client."""
import logging

from notifiers.notifier import Notifier

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
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}%parse_mode=html"

    def notify(self, msg: str) -> None:
        try:
            requests.post(self.url + f'&text={msg}')
        except requests.exceptions.RequestException as e:
            logging.error(e)

    def get_updates(self):
        url = f'https://api.telegram.org/bot{self.token}/getUpdates'
        resp = requests.get(url)
        logging.info(resp.json())
