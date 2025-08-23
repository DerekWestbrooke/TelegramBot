import asyncio
import datetime
import re
import threading
import hashlib

from datetime import timedelta
from resources.values import regex_notify
from resources.user_logger import create_local_logger

user_logger = create_local_logger()


# Функция для преобразования массива населенных пунктов в строку
def sort_locations_list(locations_list):
    new_locations_list = []
    new_locations_list.append("Беларусь") if "Беларусь" in locations_list else None
    new_locations_list.extend(
        [
            i
            for i in [
                "Брестская область",
                "Витебская область",
                "Гомельская область",
                "Гродненская область",
                "Минская область",
                "Могилёвская область",
            ]
            if i in locations_list
        ]
    )
    new_locations_list.extend(
        sorted([i for i in locations_list if i not in new_locations_list])
    )
    return "\n".join([f"{i+1}. {value}" for i, value in enumerate(new_locations_list)])


# Функция, показывающая действие бота
async def show_status_typing(using_bot, chat_id, sec=1):
    await using_bot.send_chat_action(chat_id, action="typing")
    await asyncio.sleep(sec)


# Функция потока для мониторинга объявлений
def start_searching_site_advs_thread(parser_object, city, min_sum, max_sum, additional):
    threading.Thread(
        target=parser_object.start_kufar_parsing,
        args=(city, min_sum, max_sum, additional),
        daemon=True,
    ).start()


# Преобразование в datetime
def create_datetime(year, month, day, hour, minute):
    try:
        return datetime.datetime(year, month, day, hour, minute)
    except ValueError:
        return None


# Преобразование в int для данных времени
def return_int_value(value):
    if value is not None:
        return int(value)
    else:
        return None


# Функция создания периода времени для оповещения об оплате счетов ЖКХ
def parse_notify_datetime(input_datetime):
    m = re.match(regex_notify, input_datetime)
    hour = return_int_value(m.group(1))
    minute = return_int_value(m.group(2))
    day = return_int_value(m.group(3))
    month = return_int_value(m.group(4))
    year = return_int_value(m.group(5))
    start_day = return_int_value(m.group(6))
    start_month = return_int_value(m.group(7))
    start_year = return_int_value(m.group(8))
    end_day = return_int_value(m.group(9))
    end_month = return_int_value(m.group(10))
    end_year = return_int_value(m.group(11))

    if day and month and year:
        datetime_to_notify = create_datetime(year, month, day, hour, minute)
        return datetime_to_notify, datetime_to_notify + timedelta(minutes=1)
    elif all([start_day, start_month, start_year, end_day, end_month, end_year]):
        start_datetime_to_notify = create_datetime(
            start_year, start_month, start_day, hour, minute
        )
        end_datetime_to_notify = create_datetime(
            end_year, end_month, end_day, hour, minute
        )
        if end_datetime_to_notify > start_datetime_to_notify:
            return start_datetime_to_notify, end_datetime_to_notify
        else:
            return end_datetime_to_notify, start_datetime_to_notify
    else:
        return None


# Функция хеширования айди пользователя
def get_user_id_hash(user_id_str):
    user_id_hash = hashlib.sha256(str(user_id_str).encode("utf-8")).hexdigest()
    return user_id_hash
