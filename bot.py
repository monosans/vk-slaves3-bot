#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import uniform
from sys import stderr
from threading import Thread
from time import sleep, time

from loguru import logger

from api import Slaves3
from config import (
    AUTHORIZATION,
    BUY_FROM_IDS,
    BUY_SLAVES_MODE,
    MAX_DELAY,
    MAX_PRICE,
    MIN_DELAY,
    MIN_PRICE,
    SET_FETTERS,
    TOP_EXCLUDE,
    USER_AGENT,
)


def sleep_delay() -> None:
    sleep(uniform(MIN_DELAY, MAX_DELAY))


def get_bonus() -> None:
    """Получение бонуса."""
    while True:
        earn = client.earn()
        try:
            balance = earn["balance"]
            logger.info(
                f"""
Бонус получен
Баланс: {balance['coins']}
Цепей: {balance['fetters']}"""
            )
            sleep(61 + uniform(0, 2))
        except KeyError:
            sleep_delay()


def buy_target_slaves(target_id: int) -> None:
    """Перекупка рабов у target_id."""
    slave_list = client.slave_list(target_id)
    have_bought = False
    if slave_list:
        for slave in slave_list["list"]:
            price = slave["price"]
            if (
                slave["was_in_app"]
                and MIN_PRICE <= price <= MAX_PRICE
                and slave["fetter_to"] < time()
            ):
                slave_id = slave["vk_user_id"]
                buy_slave = client.buy_slave(slave_id)
                if buy_slave:
                    me = buy_slave["user"]
                    logger.info(
                        f"""
Купил id{slave_id} за {price} у id{target_id}
Баланс: {me['balance']['coins']}
Рабов: {me['slaves_count']}
Доход в минуту: {me['slaves_profit_per_min']}"""
                    )
                    if SET_FETTERS == 1 and client.set_fetters(slave_id):
                        logger.info(f"Заковал id{slave_id}")
                have_bought = True
                sleep_delay()
    if not have_bought:
        sleep_delay()


def buy_top_users_slaves() -> None:
    """Перекупка рабов у топеров."""
    while True:
        top_users = (
            client.top_users_refs()
            if BUY_SLAVES_MODE == 1
            else client.top_users()
        )
        if top_users:
            for top_user in top_users["list"]:
                user_id = top_user["vk_user_id"]
                if user_id != MY_ID and user_id not in TOP_EXCLUDE:
                    buy_target_slaves(user_id)
        else:
            sleep_delay()


def buy_slaves_from_ids() -> None:
    """Перекупка рабов у BUY_FROM_IDS из config.py."""
    while True:
        for user_id in BUY_FROM_IDS:
            buy_target_slaves(user_id)


def buy_fetters() -> None:
    """Заковывание имеющихся рабов."""
    while True:
        slave_list = client.slave_list(MY_ID)
        if slave_list:
            for slave in slave_list["list"]:
                if slave["fetter_to"] < time():
                    slave_id = slave["vk_user_id"]
                    if client.set_fetters(slave_id):
                        logger.info(f"Заковал id{slave_id}")
                    sleep_delay()
        else:
            sleep_delay()


if __name__ == "__main__":
    logger.remove()
    logger.add(
        stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>",
        colorize=True,
    )
    client = Slaves3(
        AUTHORIZATION.strip(), USER_AGENT.strip(), MIN_DELAY, MAX_DELAY
    )
    MY_ID = client.earn()["earning"]["vk_user_id"]
    if BUY_SLAVES_MODE == 0:
        if SET_FETTERS == 1:
            Thread(target=buy_fetters).start()
    elif BUY_SLAVES_MODE in {1, 2}:
        Thread(target=buy_top_users_slaves).start()
    elif BUY_SLAVES_MODE == 3:
        Thread(target=buy_slaves_from_ids).start()
    sleep_delay()
    Thread(target=get_bonus).start()
