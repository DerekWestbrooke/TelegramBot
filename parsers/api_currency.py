import requests

from resources.values import currency_info
from resources.database import create_local_logger

user_logger = create_local_logger()


# Функция получения информации о курсах валют
def get_exchange_rates():
    url = "https://api.nbrb.by/exrates/rates?periodicity=0"
    currency_dict = dict()
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        rates = response.json()
        for rate in rates:
            code = rate["Cur_Abbreviation"]
            if code in currency_info:
                country, currency_name, emoji = currency_info.get(code)
                currency_dict[code] = (
                    emoji,
                    country,
                    currency_name,
                    rate["Cur_OfficialRate"],
                    rate["Cur_Scale"],
                )
        user_logger.info(f"Получение информации о курсах валют проведено успешно")
    else:
        currency_dict = None
        user_logger.warning(
            f"Получение информации о курсах валют отменено ({response.status_code})"
        )
    return currency_dict
