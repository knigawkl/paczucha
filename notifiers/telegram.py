"""This module contains a class capable of interacting with Telegram's API."""
import logging
from typing import Optional

import requests


class Telegram:
    """Telegram client."""
    TIMEOUT = 5

    def __init__(self, token: str, chat_id: int) -> None:
        """Instantiates a telegram client. No healthcheck is performed.

        Args:
             token: Each bot is given a unique authentication token when it is created.
             chat_id: Unique identifier for the target chat. Example: 0.

        """
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}/"

    def notify(self, msg: str) -> Optional[str]:
        """Notify via Telegram.

        Args:
            msg: The message to be sent.

        Returns:
            Identifier of the message sent.

        """
        url = f'{self.url}sendMessage?chat_id={self.chat_id}%parse_mode=html&text={msg}'
        try:
            resp = requests.post(url, timeout=Telegram.TIMEOUT).json()
            return str(resp.get('result', {}).get('message_id'))
        except requests.exceptions.RequestException as exception:
            logging.error(exception)
            return None

    def delete(self, msg_id: int) -> None:
        """Delete a Telegram message.

        Args:
            msg_id: Telegram message identifier.

        """
        url = f'{self.url}deleteMessage?chat_id={self.chat_id}&message_id={msg_id}'
        try:
            requests.post(url, timeout=Telegram.TIMEOUT)
        except requests.exceptions.RequestException as exception:
            logging.error(exception)

    def _get_updates(self):
        """Receive incoming updates using long polling."""
        url = f'{self.url}getUpdates'
        resp = requests.get(url, timeout=Telegram.TIMEOUT)
        logging.info(resp.json())
