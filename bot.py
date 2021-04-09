#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import uniform
from threading import Thread
from time import sleep, strftime

from requests import get, post

from config import (
    authorization,
    buy_from_ids,
    buy_slaves_mode,
    max_delay,
    max_price,
    min_delay,
    min_price,
    my_id,
    set_fetters,
)


def get_bonus():
    """Получает бонус."""
    post(
        "https://slave.su/api/bonuses/earn",
        headers=headers,
        json={"type": "bonus:rewarded_ad"},
    )


def get_buy_slave(id):
    """Покупает раба."""
    return post(
        "https://slave.su/api/slaves/buySlave",
        headers=headers,
        json={"slave_id": id},
    ).json()


def get_user(id):
    """Возвращает информацию о пользователе."""
    return get(
        f"https://slave.su/api/slaves/user/{id}",
        headers=headers,
    ).json()


def get_slave_list(id):
    """Возвращает список рабов пользователя."""
    return get(
        f"https://slave.su/api/slaves/slaveList/{id}",
        headers=headers,
    ).json()


def get_top_users():
    """Возвращает список топ игроков."""
    return get(
        "https://slave.su/api/slaves/topUsers",
        headers=headers,
    ).json()


def get_set_fetter(id):
    """Надевает на раба оковы."""
    return post(
        "https://slave.su/api/slaves/setFetters",
        headers=headers,
        json={"slave_id": id},
    ).json()


def get_bonuses():
    while True:
        try:
            get_bonus()
            print("Бонус получен")
            sleep(60 + uniform(0, 3.34))
        except Exception as e:
            print(e.args)
            sleep(3.34)


def buy_top_users_slaves():
    """Перекупает рабов у топеров."""
    try:
        top_users = get_top_users()
        if "list" in top_users.keys():
            for top_user in top_users["list"]:
                top_user_slaves = get_slave_list(top_user["vk_user_id"])
                if "list" in top_user_slaves.keys():
                    for slave in top_user_slaves["list"]:
                        if slave["fetter_to"] == 0:
                            if (
                                slave["price"] <= max_price
                                and slave["price"] >= min_price
                            ):
                                get_bonus()
                                buy_slave_info = get_buy_slave(
                                    slave["vk_user_id"],
                                )
                                if "user" in buy_slave_info.keys():
                                    profile = buy_slave_info["user"]
                                    print(
                                        f"""[{strftime('%H:%M:%S')}]
Купил id{slave['vk_user_id']} за {slave['price']} у id{top_user['vk_user_id']}
Баланс: {'{:,}'.format(profile['balance']['coins'])}
Рабов: {profile['slaves_count']}
Доход в минуту: {profile['slaves_profit_per_min']}""",
                                    )
                                    if set_fetters == 1:
                                        fetter = get_set_fetter(
                                            slave["vk_user_id"],
                                        )
                                        if "error" not in fetter.keys():
                                            print(
                                                f"Надел оковы id{slave['vk_user_id']}",
                                            )
                                sleep(uniform(min_delay, max_delay))
                else:
                    sleep(3.34)
        else:
            sleep(3.34)
    except Exception as e:
        print(e.args)
        sleep(3.34)


def buy_slaves_from_ids():
    """Перекупает рабов у ID из config.py."""
    try:
        for id in buy_from_ids:
            slaves = get_slave_list(id)
            if "list" in slaves.keys():
                for slave in slaves["list"]:
                    if slave["fetter_to"] == 0:
                        if (
                            slave["price"] <= max_price
                            and slave["price"] >= min_price
                        ):
                            get_bonus()
                            buy_slave_info = get_buy_slave(slave["vk_user_id"])
                            if "user" in buy_slave_info.keys():
                                profile = buy_slave_info["user"]
                                print(
                                    f"""[{strftime('%H:%M:%S')}]
Купил id{slave['vk_user_id']} за {slave['price']} у id{id}
Баланс: {'{:,}'.format(profile['balance']['coins'])}
Рабов: {profile['slaves_count']}
Доход в минуту: {profile['slaves_profit_per_min']}""",
                                )
                                if set_fetters == 1:
                                    fetter = get_set_fetter(
                                        slave["vk_user_id"],
                                    )
                                    if "error" not in fetter.keys():
                                        print(
                                            f"Надел оковы id{slave['vk_user_id']}",
                                        )
                            sleep(uniform(min_delay, max_delay))
            else:
                sleep(3.34)
    except Exception as e:
        print(e.args)
        sleep(3.34)


def buy_fetters():
    """Надевает оковы."""
    while True:
        try:
            slaves = get_slave_list(my_id)
            flag = 0
            if "list" in slaves.keys():
                for slave in slaves["list"]:
                    if slave["fetter_to"] == 0:
                        flag = 1
                        fetter = get_set_fetter(slave["vk_user_id"])
                        if "error" not in fetter.keys():
                            print(
                                f"Надел оковы id{slave['vk_user_id']}",
                            )
                        sleep(uniform(min_delay, max_delay))
                if flag == 0:
                    sleep(3.34)
            else:
                sleep(3.34)
        except Exception as e:
            print(e.args)
            sleep(3.34)


if __name__ == "__main__":
    print(
        """ВРабстве 3.0
vk.com/free_slaves_bot
github.com/monosans/vk-slaves3-bot
Версия 20210410.1""",
    )
    headers = {
        "Content-Type": "application/json",
        "authorization": authorization,
        "origin": "https://stage-app7790408-d3d98043d3c2.pages.vk-apps.com",
        "referer": "https://stage-app7790408-d3d98043d3c2.pages.vk-apps.com/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.51 Safari/537.36",
    }
    if buy_slaves_mode == 1:
        print("Включена перекупка у топеров")
        while True:
            buy_top_users_slaves()
    elif buy_slaves_mode == 2:
        print("Включена перекупка у buy_from_ids из config.py")
        while True:
            buy_slaves_from_ids()
    elif buy_slaves_mode == 0 and set_fetters == 0:
        print("Включено получение бонуса")
        get_bonuses()
    elif buy_slaves_mode == 0 and set_fetters == 1:
        print("Включены получение бонуса и надевание оков")
        Thread(target=get_bonuses).start()
        Thread(target=buy_fetters).start()
