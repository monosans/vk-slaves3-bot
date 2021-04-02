#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from json import load
from random import randint, uniform
from time import sleep, strftime

from requests import get, post


def buy_slave(id):
    """Покупает раба."""
    post(
        "https://slaves-mini-app.xyz/api/slaves/buySlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": user_agent,
            "origin": origin,
        },
        json={"slave_id": id},
    )


def get_buy_slave(id):
    """Покупает раба."""
    return post(
        "https://slaves-mini-app.xyz/api/slaves/buySlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": user_agent,
            "origin": origin,
        },
        json={"slave_id": id},
    ).json()


def get_user(id):
    """Получает информацие о пользователе."""
    return get(
        f"https://slaves-mini-app.xyz/api/slaves/user/{id}",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": user_agent,
            "origin": origin,
        },
    ).json()


def get_slave_list(id):
    """Возвращает список рабов пользователя."""
    return get(
        f"https://slaves-mini-app.xyz/api/slaves/slaveList/{id}",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": user_agent,
            "origin": origin,
        },
    ).json()


def get_top_users():
    """Возвращает список топ игроков."""
    return get(
        "https://slaves-mini-app.xyz/api/slaves/topUsers",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": user_agent,
            "origin": origin,
        },
    ).json()


def buy_top_users_slaves():
    """То же самое, что и buy_slaves, только перекупает рабов у топ игроков."""
    try:
        top_users = get_top_users()
        if "list" in top_users.keys():
            for top_user in top_users["list"]:
                top_user_slaves = get_slave_list(top_user["vk_user_id"])
                if "list" in top_user_slaves.keys():
                    for slave in top_user_slaves["list"]:
                        slave_id = slave["vk_user_id"]
                        slave_info = get_user(slave_id)
                        if "price" in slave_info.keys():
                            if (
                                slave_info["price"] <= max_price
                                and slave_info["price"] >= min_price
                            ):
                                # Покупка раба
                                buy_slave_info = get_buy_slave(slave_id)

                                if "user" in profile.keys():
                                    profile = buy_slave_info["user"]
                                    print(
                                        f"""\n==[{strftime("%d.%m.%Y %H:%M:%S")}]==
Купил id{slave_info['vk_user_id']} за {slave_info['price']} у id{top_user['vk_user_id']}
Баланс: {"{:,}".format(profile['balance']['coins'])}
Рабов: {"{:,}".format(profile['slaves_count'])}
Доход в минуту: {"{:,}".format(profile['slaves_profit_per_min'])}\n"""
                                    )
                                    sleep(uniform(min_delay, max_delay))
    except Exception as e:
        print(e.args)
        sleep(uniform(min_delay, max_delay))


def buy_slaves():
    """Покупает и улучшает рабов, надевает оковы, если включено в config.json."""
    try:
        # Случайный раб в промежутке
        slave_id = randint(1, 647360748)
        slave_info = get_user(slave_id)

        # Проверка раба на соотвествие настройкам цены
        while (
            slave_info["price"] > max_price or slave_info["price"] < min_price
        ):
            slave_id = randint(1, 647360748)
            slave_info = get_user(slave_id)

        # Покупка раба
        buy_slave_info = get_buy_slave(slave_id)

        if "user" in profile.keys():
            profile = buy_slave_info["user"]
            print(
                f"""\n==[{strftime("%d.%m.%Y %H:%M:%S")}]==
Купил id{slave_info['vk_user_id']} за {slave_info['price']}
Баланс: {"{:,}".format(profile['balance']['coins'])}
Рабов: {"{:,}".format(profile['slaves_count'])}
Доход в минуту: {"{:,}".format(profile['slaves_profit_per_min'])}\n""",
            )
            sleep(uniform(min_delay, max_delay))
    except Exception as e:
        print(e.args)
        sleep(uniform(min_delay, max_delay))


def buy_from_ids():
    """То же самое, что и buy_slaves, только перекупает рабов из списка в config.json."""
    try:
        for id in buy_from_ids_list:
            slaves = get_slave_list(id)
            if "list" in slaves.keys():
                for slave in slaves["list"]:
                    slave_id = slave["vk_user_id"]
                    slave_info = get_user(slave_id)
                    if "price" in slave_info.keys():
                        if (
                            slave_info["price"] <= max_price
                            and slave_info["price"] >= min_price
                        ):
                            # Покупка раба
                            buy_slave_info = get_buy_slave(slave_id)

                            if "user" in profile.keys():
                                profile = buy_slave_info["user"]
                                print(
                                    f"""\n==[{strftime("%d.%m.%Y %H:%M:%S")}]==
Купил id{slave_info['vk_user_id']} за {slave_info['price']} у id{id}
Баланс: {"{:,}".format(profile['balance']['coins'])}
Рабов: {"{:,}".format(profile['slaves_count'])}
Доход в минуту: {"{:,}".format(profile['slaves_profit_per_min'])}\n""",
                                )
                                sleep(uniform(min_delay, max_delay))
    except Exception as e:
        print(e.args)
        sleep(uniform(min_delay, max_delay))


if __name__ == "__main__":
    print(
        """vk.com/free_slaves_bot
github.com/monosans/vk-slaves3-bot
Версия 1.0""",
    )

    # Конфиг
    with open("config.json") as f:
        try:
            config = load(f)
        except:
            print("Конфиг настроен некорректно.")
            sys.exit()
    auth = str((config["authorization"]).strip())
    buy_slaves_mode = int(config["buy_slaves_mode"])
    min_delay = int(config["min_delay"])
    max_delay = int(config["max_delay"])
    min_price = int(config["min_price"])
    max_price = int(config["max_price"])
    buy_from_ids_list = list(config["buy_from_ids"])
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36"
    origin = "https://slaves-mini-app.xyz"

    # Запуск
    if buy_slaves_mode == 1:
        print("Включена покупка случайных рабов.")
        while True:
            buy_slaves()
    elif buy_slaves_mode == 2:
        print("Включена перекупка рабов у топеров.")
        while True:
            buy_top_users_slaves()
    elif buy_slaves_mode == 3:
        print("Включена перекупка у IDшников из config.json.")
        while True:
            buy_from_ids()
