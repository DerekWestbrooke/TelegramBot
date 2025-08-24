import requests
import os

from dotenv import load_dotenv
from resources.database import create_local_logger
from resources.values import message_neural_network_not_found, NEURAL_NETWORK_API_KEY

user_logger = create_local_logger()


def is_api_exist():
    return True if NEURAL_NETWORK_API_KEY is not None else False


# Функция общения с нейросетью через API
def send_user_message_to_neural_network(user_text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {NEURAL_NETWORK_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": str(user_text)}],
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, json=data, timeout=10)
    if response.status_code == 200:
        json_resp = response.json()
        user_logger.info(f"Связь с нейросетью проведена успешно")
        return json_resp["choices"][0]["message"]["content"]
    else:
        user_logger.warning(
            f"Ошибка установки связи с нейросетью ({response.status_code})"
        )
        return message_neural_network_not_found
