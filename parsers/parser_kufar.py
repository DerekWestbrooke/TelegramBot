import asyncio
import time
import random

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from resources.values import *
from resources.bot_keyboards import estate_kufar_stop_button
from resources.database import create_local_logger

user_logger = create_local_logger()


# Класс для парсинга сайта Kufar
class KufarParser:
    # Конструктор класса
    def __init__(self, activity=None, bot=None, chat_id=None, loop=None):
        super().__init__()

        self.bot = bot
        self.chat_id = chat_id
        self.loop = loop
        self.activity = activity
        self.currency = ""
        self.location = ""
        self.price_min = 0
        self.price_max = 0
        self.url = "https://re.kufar.by/?elementType=categories&_gl=1*1phpw7u*_gcl_au*NDg5NzQ5NzU4LjE3NTI1NzI2NTc.*_ga*MjEyNTk2ODA2Ny4xNzUyNTcyNjMy*_ga_ESH3WRCK3J*czE3NTI1NzI2NTgkbzEkZzEkdDE3NTI1NzI4NTgkajUyJGwwJGgw"
        self.user_agent = UserAgent()
        self.webdriver = None
        self.wait = None
        self.last_adv_id = None
        self.last_adv_url = None
        self.keep_running = False

    # Задание настроек для браузера Selenium
    def set_drivers(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument(f"user-agent={self.user_agent.random}")
        options.add_argument("--window-size=945,1028")
        self.webdriver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.webdriver, 10)
        user_logger.info(f"Kufar: установка настроек")

    # Получение куки
    def get_cookies(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div/button")
                )
            ).click()
            user_logger.info(f"Kufar: куки приняты")
        except TimeoutError:
            user_logger.warning(f"Kufar: ошибка получения куки")

    # Открытие сайта
    def open_web_site(self):
        self.webdriver.get(self.url)
        time.sleep(random.uniform(0.5, 2))
        user_logger.info(f"Kufar: сайт открыт")

    # Завершение работы драйвера
    def close_webdriver(self):
        if self.webdriver:
            self.webdriver.quit()
        user_logger.info(f"Kufar: завершение работы драйвера")

    # Получение списка населенных пунктов
    def get_locations_names(self):
        try:
            self.set_drivers()
            self.open_web_site()
            self.get_cookies()
            self.webdriver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[1]/main/div/div/div[1]/div/div/div[2]/div[1]/section/button",
            ).click()
            buttons_locations_list = self.webdriver.find_elements(
                By.CLASS_NAME, "styles_button__TMqNk"
            )
            locations_names = [i.text for i in buttons_locations_list]
            user_logger.info(f"Kufar: получение списка местоположений")
            return locations_names
        except Exception as e:
            user_logger.info(f"Kufar: ошибка получения списка местоположений ({e})")
            return None

    # Задание фильтра для отбора объявлений
    def set_filter(self, city, min_price, max_price, currency):
        try:
            self.set_drivers()
            self.open_web_site()
            self.get_cookies()
        except Exception as e:
            user_logger.warning(
                f"Kufar: ошибка на этапе подготовке к мониторингу ({e})"
            )
        if self.activity == "Rent":
            try:
                element_rent = self.webdriver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div[2]/div[1]/main/div/div/div[1]/div/div/div[1]/div[2]",
                )
                element_rent.click()
                time.sleep(random.uniform(0.5, 2))
                user_logger.info(f"Kufar: выбор аренды квартиры")
            except Exception as e:
                user_logger.warning(
                    f"Kufar: не удалось выбрать пункт для аренды квартиры ({e})"
                )
        elif self.activity == "Purchase":
            try:
                element_purchase = self.webdriver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div[2]/div[1]/main/div/div/div[1]/div/div/div[1]/div[1]",
                )
                element_purchase.click()
                time.sleep(random.uniform(0.5, 2))
                user_logger.info(f"Kufar: выбор покупка квартиры")
            except Exception as e:
                user_logger.warning(
                    f"Kufar: не удалось выбрать пункт для покупки квартиры ({e})"
                )
        try:
            element_location = self.webdriver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[1]/main/div/div/div[1]/div/div/div[2]/div[1]/section/button",
            )
            element_location.click()
            element_div_location = self.webdriver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[1]/main/div/div/div[1]/div/div/div[2]/div[1]/section/div/div[2]/div/div[2]/div",
            )
            buttons_location = element_div_location.find_elements(By.TAG_NAME, "button")
            for i in buttons_location:
                if i.text == str(city):
                    i.click()
                    break
            user_logger.info(f"Kufar: задание местоположения прошло успешно")
        except Exception as e:
            user_logger.warning(f"Kufar: не удалось задать местоположение ({e})")
        try:
            element_min_price = self.webdriver.find_element(By.ID, "prc.lower")
            element_min_price.clear()
            element_min_price.send_keys(str(min_price))
            time.sleep(random.uniform(0.5, 2))
            user_logger.info(f"Kufar: задание минимальной цены прошло успешно")
        except Exception as e:
            user_logger.warning(f"Kufar: не удалось задать минимальную цену ({e})")
        try:
            element_max_price = self.webdriver.find_element(By.ID, "prc.upper")
            element_max_price.clear()
            element_max_price.send_keys(str(max_price))
            time.sleep(random.uniform(0.5, 2))
            user_logger.info(f"Kufar: задание максимальной цены прошло успешно")
        except Exception as e:
            user_logger.warning(f"Kufar: не удалось задать максимальную цену ({e})")
        try:
            wait = WebDriverWait(self.webdriver, 5)
            element_currency = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[2]/div[1]/main/div/div/div[1]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/select",
                    )
                )
            )
            element_currency.click()
            time.sleep(random.uniform(0.5, 2))
            currency_select = Select(element_currency)
            currency_select.select_by_value(str(currency[-3:]))
            time.sleep(random.uniform(0.5, 2))
            user_logger.info(f"Kufar: задание валюты прошло успешно")
        except Exception as e:
            user_logger.warning(f"Kufar: не удалось задать валюту ({e})")

    # Функция получения id, url объявления
    def get_last_adv_id(self):
        try:
            advs_element = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'a[href][target="_blank"][data-testid="kufar-realty-card-0"]',
                    )
                )
            )
            last_adv_url = advs_element.get_attribute("href")
            user_logger.info(f"Kufar: получение ID первого объявления прошло успешно")
            return str(last_adv_url.split("/")[-1].split("?")[0]), last_adv_url
        except Exception as e:
            user_logger.warning(
                f"Kufar: получение ID первого объявления провалилось ({e})"
            )
            return None, None

    # Функция парсинга сайта
    def start_kufar_parsing(self, city, min_price, max_price, currency):
        self.keep_running = True
        try:
            self.set_filter(city, min_price, max_price, currency)
            element_launch = self.webdriver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[1]/main/div/div/div[1]/div/div/div[2]/div[3]/button[2]",
            )
            element_launch.click()
            user_logger.info(f"Kufar: запуск мониторинга прошел успешно")
        except Exception as e:
            user_logger.warning(f"Kufar: ошибка запуска мониторинга ({e})")
        time.sleep(random.uniform(0.5, 2))
        self.last_adv_id, self.last_adv_url = self.get_last_adv_id()
        while self.keep_running:
            for _ in range(60):
                if not self.keep_running:
                    break
                time.sleep(random.uniform(0.5, 2))
            self.webdriver.refresh()
            time.sleep(random.uniform(0.5, 2))
            current_adv_id, current_adv_url = self.get_last_adv_id()
            if current_adv_id != self.last_adv_id:
                try:
                    estate_descr = self.webdriver.find_element(
                        By.XPATH,
                        "/html/body/div[1]/div[2]/div[1]/main/div[1]/div/div[3]/div[1]/div[4]/div/section[1]/a/div[2]/div[1]/div[2]/div[1]",
                    ).text
                    user_logger.info(
                        f"Kufar: получение описания нового объявления прошло успешно"
                    )
                except Exception as e:
                    user_logger.warning(
                        f"Kufar: ошибка получения описания нового объявления ({e})"
                    )
                    estate_descr = "Нет данных"
                try:
                    estate_addr = self.webdriver.find_element(
                        By.XPATH,
                        "/html/body/div[1]/div[2]/div[1]/main/div[1]/div/div[3]/div[1]/div[4]/div/section[1]/a/div[2]/div[1]/div[2]/div[2]/span",
                    ).text
                    user_logger.info(
                        f"Kufar: получение адреса нового объявления прошло успешно"
                    )
                except Exception as e:
                    user_logger.warning(
                        f"Kufar: ошибка получения адреса нового объявления ({e})"
                    )
                    estate_addr = "Нет данных"
                try:
                    usd_price = self.webdriver.find_element(
                        By.XPATH,
                        "/html/body/div[1]/div[2]/div[1]/main/div[1]/div/div[3]/div[1]/div[4]/div/section[1]/a/div[2]/div[1]/div[1]/span[2]",
                    ).text
                    user_logger.info(
                        f"Kufar: получение цены в USD нового объявления прошло успешно"
                    )
                except Exception as e:
                    user_logger.warning(
                        f"Kufar: ошибка получения цены в USD нового объявления ({e})"
                    )
                    usd_price = "Нет данных"
                try:
                    byn_price = self.webdriver.find_element(
                        By.XPATH,
                        "/html/body/div[1]/div[2]/div[1]/main/div[1]/div/div[3]/div[1]/div[4]/div/section[1]/a/div[2]/div[1]/div[1]/span[1]",
                    ).text
                    user_logger.info(
                        f"Kufar: получение цены в BYN нового объявления прошло успешно"
                    )
                except Exception as e:
                    user_logger.warning(
                        f"Kufar: ошибка получения цены в BYN нового объявления ({e})"
                    )
                    byn_price = "Нет данных"

                url_to_send = current_adv_url
                self.last_adv_id = current_adv_id
                self.last_adv_url = current_adv_url
                activity = "об аренде" if self.activity == "Rent" else "о покупке"
                self.send_data_to_bot(
                    activity,
                    estate_descr,
                    estate_addr,
                    usd_price,
                    byn_price,
                    url_to_send,
                )

    # Работа в потоке
    def send_data_to_bot(self, activity, descr, address, usd_price, byn_price, url):
        if self.bot and self.loop and self.chat_id:
            asyncio.run_coroutine_threadsafe(
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message_kufar_new_adv.format(
                        activity=activity,
                        descr=descr,
                        address=address,
                        byn_price=byn_price,
                        usd_price=usd_price,
                        url=url,
                    ),
                    reply_markup=estate_kufar_stop_button(),
                ),
                loop=self.loop,
            )
        user_logger.info(f"Kufar: отправка нового объявления пользователю")

    # Остановка парсинга
    def stop_kufar_parsing(self):
        self.keep_running = False
        self.close_webdriver()
        user_logger.info(f"Kufar: остановка мониторинга")
