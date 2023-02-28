"""Telegram client."""
import logging

import requests


class Telegram:
    def __init__(self, token: str, chat_id: int) -> None:
        """

        Args:
             token:
             chat_id:

        """
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}/"

    def notify(self, msg: str) -> int:
        """Notify via Telegram.

        Args:
            msg: The message to be sent.

        Returns:
            Identifier of the message sent.

        """
        url = f'{self.url}sendMessage?chat_id={self.chat_id}%parse_mode=html&text={msg}'
        try:
            resp = requests.post(url).json()
            return resp['result']['message_id']
        except requests.exceptions.RequestException as e:
            logging.error(e)

    def delete(self, msg_id: int) -> None:
        """Delete a Telegram message.

        Args:
            msg_id: Telegram message identifier.

        """
        url = f'{self.url}deleteMessage?chat_id={self.chat_id}&message_id={msg_id}'
        try:
            requests.post(url)
        except requests.exceptions.RequestException as e:
            logging.error(e)

    def _get_updates(self):
        url = f'{self.url}getUpdates'
        resp = requests.get(url)
        logging.info(resp.json())
