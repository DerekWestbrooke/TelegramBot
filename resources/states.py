from aiogram.fsm.state import State, StatesGroup


# Класс для начального взаимодействия с ботом
class UserObject(StatesGroup):
    # 0 stage (Entrance)
    user_entrance = State()

    # 1 stage (Estate/Currency/Communal_services)
    user_object = State()


# Класс для темы валют
class CurrencyBranch(StatesGroup):
    # 3.1 stage (Currency)
    currency_activity = State()

    # 3.2 stage (Rates/Calculator)
    currency_activity_rates = State()
    currency_activity_calculator = State()

    # 3.3 stage (Convert from)
    currency_activity_calculator_from = State()

    # 3.4 stage (Convert to)
    currency_activity_calculator_from_to = State()

    # 3.5 stage (Amount)
    currency_activity_calculator_from_to_amount = State()

    # 3.6 stage (Result of calculating)
    currency_activity_calculator_from_to_amount_result = State()


# Класс для темы недвижимости
class EstateBranch(StatesGroup):
    # 2.1 stage (Rent/Purchase)
    estate_activity = State()

    # 2.2 stage (Kufar/Onliner)
    estate_activity_site = State()

    # 2.3 stage (Location)
    estate_activity_site_location = State()

    # 2.4 stage (currency)
    estate_activity_site_location_currency = State()

    # 2.5 stage (Min)
    estate_activity_site_location_currency_min = State()

    # 2.6 stage (Max)
    estate_activity_site_location_currency_min_max = State()

    # 2.7 stage (Filter)
    estate_activity_site_location_currency_min_max_filter = State()

    # 2.8 stage (Parsing)
    estate_activity_site_location_currency_min_max_filter_parsing = State()

    # 2.9 stage (Stop parsing)
    estate_activity_site_location_currency_min_max_filter_parsing_stop = State()


# Класс для темы услуг ЖКХ
class CommunalServices(StatesGroup):
    # 3.1 stage (Communal Services)
    communal_activity = State()

    # 3.2 stage (Payment/Counters/Request)
    communal_activity_payment = State()
    communal_activity_counters = State()
    communal_activity_request = State()

    # 3.3 stage (Select action below)
    communal_activity_payment_time = State()
    communal_activity_counters_show = State()
    communal_activity_counters_add = State()
    communal_activity_counters_edit = State()
    communal_activity_counters_delete = State()
    communal_activity_request_bot = State()

    # 3.4 stage (Select action below)
    communal_activity_payment_time_ok = State()
    communal_activity_counters_add_question = State()
    communal_activity_counters_edit_data = State()


# Класс для темы нейросети
class NeuralNetwork(StatesGroup):
    # 4.1 stage(Select neural network)
    neural_question = State()
    # 4.2 stage (Send question for neural network)
    neural_question_send = State()
