# Files_names
db_name = "telegram_bot_database"
log_file_name = "events.log"

# Variables
allow_flat_numbers = ["1", "2", "3", "4"]
currency_info = {
    "AUD": ("Австралия", "Австралийский доллар", "🇦🇺"),
    "AZN": ("Азербайджан", "Манат", "🇦🇿"),
    "BYN": ("Беларусь", "Белорусский рубль", "🇧🇾"),
    "BGN": ("Болгария", "Лев", "🇧🇬"),
    "HUF": ("Венгрия", "Форинт", "🇭🇺"),
    "HKD": ("Гонконг", "Гонконгский доллар", "🇭🇰"),
    "DKK": ("Дания", "Датская крона", "🇩🇰"),
    "USD": ("США", "Доллар", "🇺🇸"),
    "EUR": ("Европа", "Евро", "🇪🇺"),
    "INR": ("Индия", "Рупия", "🇮🇳"),
    "ILS": ("Израиль", "Новый шекель", "🇮🇱"),
    "JPY": ("Япония", "Иена", "🇯🇵"),
    "KZT": ("Казахстан", "Тенге", "🇰🇿"),
    "CAD": ("Канада", "Канадский доллар", "🇨🇦"),
    "QAR": ("Катар", "Катарский риал", "🇶🇦"),
    "KRW": ("Южная Корея", "Вона", "🇰🇷"),
    "CNY": ("Китай", "Юань", "🇨🇳"),
    "MDL": ("Молдова", "Лей", "🇲🇩"),
    "NOK": ("Норвегия", "Норвежская крона", "🇳🇴"),
    "PLN": ("Польша", "Злотый", "🇵🇱"),
    "RON": ("Румыния", "Лей", "🇷🇴"),
    "RUB": ("Россия", "Российский рубль", "🇷🇺"),
    "TJS": ("Таджикистан", "Сомони", "🇹🇯"),
    "TRY": ("Турция", "Лира", "🇹🇷"),
    "TMT": ("Туркменистан", "Манат", "🇹🇲"),
    "UZS": ("Узбекистан", "Сум", "🇺🇿"),
    "UAH": ("Украина", "Гривна", "🇺🇦"),
    "CZK": ("Чехия", "Крона", "🇨🇿"),
    "SEK": ("Швеция", "Шведская крона", "🇸🇪"),
    "CHF": ("Швейцария", "Швейцарский франк", "🇨🇭"),
    "GBP": ("Великобритания", "Фунт стерлингов", "🇬🇧"),
}
will_notify = False
notify_time = str()

# RegExpr
regex_notify = r"^В\s(\d{1,2}):(\d{2})\s(?:(\d{1,2})\.(\d{2})\.(\d{4})|с\s(\d{1,2})\.(\d{2})\.(\d{4})\sпо\s(\d{1,2})\.(\d{2})\.(\d{4}))$"
regex_counters = r"Э:(\d+\.?\d*);ТВ:(\d+\.?\d*);ХВ:(\d+\.?\d*)"

### Buttons_name
button_lets_chat = "🚀 Давай общаться!"
# Estate
button_estate = "🏙️ Недвижимость"
button_restart = "♻️ Перезапусти меня!"
button_rent = "🔑 Аренда"
button_purchase = "🛒 Покупка"
button_back = "↩️ Назад"
button_kufar = "💻 Kufar"
buttons_currency = ("🇧🇾 BYR", "🇺🇲 USD", "🇪🇺 EUR")
button_location = "📌 Местоположение"
button_max_price = "📈 Максимальная стоимость"
button_min_price = "📉 Минимальная стоимость"
button_launch = "🚀 Поехали!"
button_stop = "🛑 Остановись!"
button_main_menu = "🏠 Главное меню"
button_kufar_filter = "⚙️ Фильтр"
button_flat_number = "🚪 Количество комнат"
# Currency
button_exchange_rate = "💸 Курс валют"
button_calculator = "🧮 Калькулятор валют"
button_currency = "💵 Валюта"
# Communal_services
button_communal_services = "🏢 ЖКХ"
button_payment = "🔔 Напоминание об оплате "
button_counters = "📝 Учет показания счетчиков"
button_request = "📞 Контакты"
button_yes = "🟢 Да"
button_no = "🔴 Нет"
button_show_counters = "👀 Посмотреть показания счетчиков"
button_add_counters = "📝 Добавить показания счетчиков"
button_delete_counters = "🗑️ Удалить показания счетчиков"
button_write_to_db = "💾 Записать в БД"
button_change_counters = "✏️ Изменить значение"
button_record = "✒️ Запись №{number}:"
# Deepseek
button_neural_network = "🧠 Нейросеть"


### Phrases
message_press_launch_button = "🤖 Запусти меня, нажав на кнопку ниже!"
message_greeting = "🔥 <b><i>SkyOnix</i></b> приветствует тебя 🤝."
message_about_repair = "🤖 Эта функция в разработке..."
message_restart = "🤖 Я был успешно перезапущен!"
message_return = "🤖 Ты вернулся на предыдущий этап!"
message_unknown_text = "🤖 Не понимаю тебя...Нажми на нужную кнопку."
message_estate_site = "🤖 Выбери сайт, на котором осуществлять поиск квартир."
message_estate_action = "🤖 Хороший выбор! Тебя интересует аренда или покупка?"
message_select_type = "🤖 Подскажи, что тебя интересует?"
message_location = (
    "🤖 Выбери населенный пункт, который тебя интересует\n(например, Минск):\n"
)
message_edit_location = "🤖  Выбери и введи новый населенный пункт из перечня ниже, который тебя интересует\n(вводить нужно сам пункт без номера, например Минск):\n"
message_enter_currency = "🤖 Выбери валюту ниже:"
message_edit_currency = "🤖 Выбери новую валюту ниже:"
message_enter_min_cost = "🤖 Введи минимальную стоимость в {currency}:"
message_edit_min_cost = "🤖 Введи новую минимальную стоимость в {currency}:"
message_enter_max_cost = "🤖 Введи максимальную стоимость в {currency}:"
message_edit_max_cost = "🤖 Введи новую максимальную стоимость в {currency}:"
message_invalid_location = (
    "🤖 Не могу найти данный населенный пункт в списке. Введите новый:"
)
message_invalid_min = (
    "🤖 Какая-то странная сумма... Введите заново минимальную стоимость:"
)
message_invalid_max = (
    "🤖 Какая-то странная сумма... Введите заново максимальную стоимость:"
)
message_max_less_min = (
    "🤖 Максимальная сумма не может быть меньше минимальной... Введи еще раз:"
)
message_min_more_max = (
    "🤖 Минимальная сумма не может быть больше максимальной... Введи еще раз:"
)
message_invalid_currency = "🤖 Впервые вижу такую валюту... Попробуй еще раз ввести:"
message_invalid_amount = "🤖 Не знаю таких чисел... Попробуй еще раз ввести:"
message_start_to_parse = "🤖 Я тебя понял, буду следить за свежими объявлениями. Если захочешь прекратить мониторинг, нажми на кнопку ниже. Как только будет что интересное, дам тебе знать!"
message_wait_locations = "🤖 Хорошо, сейчас я зайду на сайт и поищу, где можно осуществлять поиск объявлений. Тебе придется немного подождать..."
message_filter_kufar = """🤖 Итак, условия поиска следующие:\n    
    🤝 тип сделки: {activity};
    🌃 населенный пункт: {location};
    💸 валюта: {currency};                        
    💵 минимальная сумма: {min_price};
    💵 максимальная сумма: {max_price}.\n
🛠️ Если хочешь что-то поменять, нажми на соответствующую кнопку.\n
🚀 Если же я все правильно понял, то могу начинать искать."""
message_stop_to_parse = "🤖 Фух, я закончил. Надеюсь, смог тебе помочь. Если нужно будет снова последить за выходом новых объявлений - дай мне знать."
message_kufar_new_adv = """🤖 Объявление {activity} квартиры 🤖\n
Описание: {descr};
Адрес: {address};
Цена(BYN): {byn_price};
Цена(USD): {usd_price}.\n
Ссылка на источник:
{url}
"""
message_invalid_input_text = "🤖 Не понял тебя... Попробуй еще раз!"
message_select_currency_activity = "🤖 Понял тебя! Ты хочешь ознакомиться с курсом валют или использовать калькулятор валют?"
message_exchange_rates = (
    "🤖 На данный момент в НБРБ установлены следующие курсы валют:\n\n"
)
message_input_currency_from = (
    "🤖 Введите код валюты, которую вы хотите перевести сумму\n(например, USD):\n\n"
    + ";\n".join(
        [
            value[2] + " " + key + " : " + value[0]
            for key, value in currency_info.items()
        ]
    )
    + "."
)
message_input_currency_to = (
    "🤖 Введите код валюты, в которую вы хотите перевести сумму\n(например, USD):"
)
message_input_amount = "🤖 Введите сумму денег, которую хотите конвертировать:"
message_convert_result = f"🤖 Результат конвертации:\n"
message_select_communal = "🤖 Отлично! Что именно тебя интересует?"
message_select_payment = "🤖 Ты хочешь, чтобы я напоминал тебе об оплате услуг ЖКХ?"
message_select_payment_time_and_days = """🤖 Отправь время и дни, когда я должен напомнить тебе о платежах.
(Формат:
    если несколько дней - «В 21:00 с 21.02.2025 по 25.02.2025»;
    если один день - «В 21:00 21.02.2025»)."""
message_select_payment_time_and_days_ok = (
    "🤖 Я понял, буду напоминать тебе, если сам не забуду."
)
message_select_no = "🤖 Понял, если поменяешь свое мнение, дай мне знать!"
message_invalid_payment_time = "🤖 Сложно... Посмотри на формат и напиши еще раз."
message_payment_time = "🤖 Пришло время оплатить счета!"
message_counters = "🤖 Хорошо, давай дальше."
message_input_counters = """🤖 Введите данные счетчиков в следующем формате:
Э:число;ТВ:число;ХВ:число (например, Э:1068;ТВ:312.5;ХВ:192.6), где:
    ⚡ Э - электричество;
    💧 ТВ - теплая вода;
    💧 ХВ - холодная вода."""
message_input_counters_result = """🤖 Итак, исходя из твоих данных показатели следующие:
    ⚡ электричество - {electricity};
    💧 теплая вода - {warm_water};
    💧 холодная вода - {cold_water}.
    
    Если все правильно, готов заносить в базу данных. Если хочешь - можешь поменять значение."""
message_input_counters_success = "🤖 Показания записаны успешно!"
message_show_counters = (
    "🤖 Понял. Вот твои показатели счетчиков, записанные в базу данных:\n"
)
message_pattern_counter_record = """✒️ Запись №{number}:
    ⚡ электричество = {electricity};
    💧 теплая вода = {warm_water};
    💧 холодная вода = {cold_water}.
"""
message_that_is_all = "🤖 Фух, это все твои записи!"
message_no_data = "🤖 Твоих данных нет!"
message_delete_counter = "🤖 Какие показания счетчиков ты хочешь удалить?"
message_delete_counters_success = "🤖️ Показания счетчиков удалены успешно!"
message_request_bot = """🤖 Как скажешь. Вот тебе контакты некоторых организаций,занимающихся проверкой счетчиков. Может понадобится.

    🏢 ООО «МИР СЧЕТЧИКОВ»
🗺️Адрес: г. Минск, ул. Серова, 12а
☎️Тел/факс: +375 17 365 72 50
☎️Мобильный (A1): +375 29 342 01 07
📧 E-mail: counterworld@mail.com

    🏢 УП «СЧЕТЧИКЧЕК»
🗺️Адрес: г. Минск, ул. Тростенецкая, 13
☎️Телефоны: короткий 119, +375 17 289 42 22, +375 44 598 50 73 (A1), +375 44 598 50 74 (A1), +375 29 570 59 21 (МТС)
📧 E-mail: countercheck@gmail.com

    🏢 СООО «ЗДОРОВЫЙ СЧЕТЧИК» 
🗺️Адрес: г. Минск, ул. Мехова, 15
☎️Телефон: +375 17 358 23 96
📧 E-mail: counterhealth@gmail.com
"""
message_request_bot_companies = "🤖 Выбери организацию, в которую ты хочешь, чтобы я отправил заявку на проверку счетчиков."
message_neural_wait = (
    "🤖 Хорошо, я передам вопрос нейросети, а ты побудь тут и подожди немного..."
)
message_neural_network = "🤖 Напиши мне вопрос, который ты хочешь задать нейросети."
message_neural_network_answer = "🤖 Получил ответ от нейросети:\n"
message_api_is_none = (
    "🤖 Прошу прощения, но пока нет возможности связаться с нейросетью."
)
message_neural_network_not_found = (
    "🤖 Хмм... Не смог найти нейросеть, давай попробуем позже."
)
### Callback_data
cd_start_bot = "start_bot"
# Estate
cd_estate = "choose_estate"
cd_rent = "choose_rent"
cd_purchase = "choose_purchase"
cd_kufar = "choose_kufar"
cd_currencies = [f"currency_{currency[-3:]}" for currency in buttons_currency]
cd_edit_location = "edit_location"
cd_edit_currency = "edit_currency"
cd_edit_min_price = "edit_min_price"
cd_edit_max_price = "edit_max_price"
cd_start_parsing = "start_parsing"
cd_stop_parsing = "stop_parsing"
cd_main_menu = "main_menu"
cd_currency_main_menu = "currency_main_menu"
cd_kufar_edit_filter = "kufar_edit_filter"
# Currency
cd_currency = "choose_currency"
cd_exchange_rate = "select_exchange_rate"
cd_calculator = "select_calculator"
# Communal_service
cd_communal = "communal_action_buttons"
cd_payment = "select_payment"
cd_counters = "select_counters"
cd_request = "select_request"
cd_yes = "select_yes"
cd_no = "select_no"
cd_add_counter = "communal_counters_add_buttons"
cd_delete_counter = "select_delete_counters"
cd_show_counter = "select_show_counters"
cd_counter_to_db = "select_write_to_db"
cd_change_counters = "select_change_counters"
cd_records_buttons_list = ["select_record_" + str(i) for i in range(1, 6)]
cd_neural_network = "select_neural_network"
