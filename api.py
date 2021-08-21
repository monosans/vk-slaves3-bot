# -*- coding: utf-8 -*-
from random import uniform
from time import sleep

from loguru import logger
from requests import Session


class Slaves3:
    def __init__(
        self,
        authorization: str,
        user_agent: str,
        min_delay: float = 6,
        max_delay: float = 8,
    ) -> None:
        """
        authorization (str): Bearer ...
        user_agent (str): User agent браузера.
        min_delay (float): Мин. задержка между одинаковыми запросами в
            секундах.
        max_delay (float): Макс. задержка между одинаковыми запросами в
            секундах.
        """
        self._s = Session()
        self._s.headers.update(
            {
                "authorization": authorization,
                "origin": "https://prod-app7790408-4cd26f60a56a.pages-ac.vk-apps.com",
                "referer": "https://prod-app7790408-4cd26f60a56a.pages-ac.vk-apps.com/",
                "user-agent": user_agent,
            }
        )
        self._MIN_DELAY = min_delay
        self._MAX_DELAY = max_delay

    def buy_slave(self, slave_id: int) -> dict:
        """Покупка раба."""
        return self._req("slaves/buySlave", "slave", {"slave_id": slave_id})

    def earn(self) -> dict:
        """Получение бонуса."""
        return self._req(
            "bonuses/earn", "earning", {"type": "bonus:rewarded_ad"}
        )

    def me(self) -> dict:
        """Получение подробной информации о себе."""
        return self._req("slaves/user/me", "user")

    def sell_slave(self, slave_id: int) -> dict:
        """Продажа раба."""
        return self._req("slaves/sellSlave", "slave", {"slave_id": slave_id})

    def set_fetters(self, slave_id: int) -> dict:
        """Надевание оков."""
        return self._req(
            "slaves/setFetters", "slave", {"gold": False, "slave_id": slave_id}
        )

    def slave_list(self, user_id: int) -> dict:
        """Получение списка рабов пользователя."""
        return self._req(f"slaves/slaveList/{user_id}", "list")

    def top_users(self) -> dict:
        """Получение игроков из топа баланса."""
        return self._req("slaves/topUsers", "list")

    def top_users_refs(self) -> dict:
        """Получение игроков из топа рабов за день."""
        return self._req("slaves/topUsersRefs", "list")

    def upgrade_slave(self, slave_id: int) -> dict:
        """Улучшение раба."""
        return self._req(
            "slaves/upgradeSlave", "slave", {"slave_id": slave_id}
        )

    def user(self, user_id: int) -> dict:
        """Получение информации о пользователе."""
        return self._req(f"slaves/user/{user_id}", "balance")

    def _req(
        self, endpoint: str, key_to_check: str, json: dict = None
    ) -> dict:
        """Метод для отправки запросов серверу игры.

        Args:
            endpoint (str): Конечная точка.
            key_to_check (str): Ключ, наличие которого проверять в ответе
                сервера, чтобы убедиться в правильности ответа.
            json (dict, optional): Данные для отправки в запросе.
                Если равен None (по умолчанию), отправляется GET запрос,
                иначе POST.

        Returns:
            dict: Если key_to_check есть в ответе сервера, возвращает ответ,
                иначе {}.
        """
        try:
            r = self._s.request(
                "GET" if json is None else "POST",
                f"https://slave.su/api/{endpoint}",
                json=json,
            ).json()
        except Exception as e:
            logger.error(f"{endpoint}: {e}")
            sleep(uniform(self._MIN_DELAY, self._MAX_DELAY))
            return self._req(endpoint, key_to_check, json)
        if key_to_check in r:
            return r
        try:
            error_message = r["error"]["message"]
        except KeyError:
            logger.error(f"{endpoint}: {r}")
        else:
            if "часто" in error_message:
                sleep(uniform(self._MIN_DELAY, self._MAX_DELAY))
                return self._req(endpoint, key_to_check, json)
            logger.error(f"{endpoint}: {error_message}")
        return {}
