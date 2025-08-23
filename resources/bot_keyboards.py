from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from resources.values import *


# GENERAL_BUTTONS: Launch button
def start_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_lets_chat, callback_data=cd_start_bot)]
        ]
    )
    return kb


# GENERAL_BUTTONS: Flats/Currency/Communal_service Buttons
def select_theme_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_estate, callback_data=cd_estate)],
            [InlineKeyboardButton(text=button_currency, callback_data=cd_currency)],
            [
                InlineKeyboardButton(
                    text=button_communal_services, callback_data=cd_communal
                )
            ],
            [
                InlineKeyboardButton(
                    text=button_neural_network, callback_data=cd_neural_network
                )
            ],
        ]
    )
    return kb


# GENERAL_BUTTONS: Main Menu button
def main_menu_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_main_menu, callback_data=cd_main_menu)]
        ]
    )
    return kb


# ESTATE: Main menu
def estate_main_menu_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_estate, callback_data=cd_estate)]
        ]
    )
    return kb


# ESTATE: Rent/Purchase Buttons
def estate_activity_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_rent, callback_data=cd_rent)],
            [InlineKeyboardButton(text=button_purchase, callback_data=cd_purchase)],
            [InlineKeyboardButton(text=button_main_menu, callback_data=cd_main_menu)],
        ]
    )
    return kb


# ESTATE: Kufar/Onliner/Back Buttons
def estate_site_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_kufar, callback_data=cd_kufar)],
            [InlineKeyboardButton(text=button_estate, callback_data=cd_estate)],
        ]
    )
    return kb


# ESTATE: Currency Buttons
def estate_currency_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=buttons_currency[0], callback_data=cd_currencies[0]
                ),
                InlineKeyboardButton(
                    text=buttons_currency[1], callback_data=cd_currencies[1]
                ),
                InlineKeyboardButton(
                    text=buttons_currency[2], callback_data=cd_currencies[2]
                ),
            ],
            [InlineKeyboardButton(text=button_estate, callback_data=cd_estate)],
        ]
    )
    return kb


# ESTATE: Filter Kufar Buttons
def estate_kufar_filter_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_location, callback_data=cd_edit_location
                ),
                InlineKeyboardButton(
                    text=button_currency, callback_data=cd_edit_currency
                ),
            ],
            [
                InlineKeyboardButton(
                    text=button_min_price, callback_data=cd_edit_min_price
                ),
                InlineKeyboardButton(
                    text=button_max_price, callback_data=cd_edit_max_price
                ),
            ],
            [InlineKeyboardButton(text=button_launch, callback_data=cd_start_parsing)],
            [InlineKeyboardButton(text=button_estate, callback_data=cd_estate)],
        ]
    )
    return kb


# ESTATE: Stop Parsing Kufar buttons
def estate_kufar_stop_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_stop, callback_data=cd_stop_parsing)]
        ]
    )
    return kb


# ESTATE: Stop Parsing Kufar Back buttons
def estate_kufar_stop_back_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_kufar_filter, callback_data=cd_kufar_edit_filter
                )
            ],
            [InlineKeyboardButton(text=button_estate, callback_data=cd_estate)],
        ]
    )
    return kb


# CURRENCY: Calculator and Exchange Rate buttons
def currency_action_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_exchange_rate, callback_data=cd_exchange_rate
                )
            ],
            [InlineKeyboardButton(text=button_calculator, callback_data=cd_calculator)],
            [InlineKeyboardButton(text=button_main_menu, callback_data=cd_main_menu)],
        ]
    )
    return kb


# CURRENCY: Main menu
def currency_main_menu_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_currency, callback_data=cd_currency)]
        ]
    )
    return kb


# COMMUNAL: Main menu
def communal_main_menu_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_communal_services, callback_data=cd_communal
                )
            ]
        ]
    )
    return kb


# COMMUNAL_SERVICE: Action buttons
def communal_action_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_payment, callback_data=cd_payment)],
            [InlineKeyboardButton(text=button_counters, callback_data=cd_counters)],
            [InlineKeyboardButton(text=button_request, callback_data=cd_request)],
            [InlineKeyboardButton(text=button_main_menu, callback_data=cd_main_menu)],
        ]
    )
    return kb


# COMMUNAL_SERVICE: Remind question buttons
def communal_remind_question_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=button_yes, callback_data=cd_yes),
                InlineKeyboardButton(text=button_no, callback_data=cd_communal),
            ],
            [
                InlineKeyboardButton(
                    text=button_communal_services, callback_data=cd_communal
                )
            ],
        ]
    )
    return kb


# COMMUNAL_SERVICE: Counters actions buttons
def communal_counters_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_show_counters, callback_data=cd_show_counter
                )
            ],
            [
                InlineKeyboardButton(
                    text=button_add_counters, callback_data=cd_add_counter
                )
            ],
            [
                InlineKeyboardButton(
                    text=button_delete_counters, callback_data=cd_delete_counter
                )
            ],
            [
                InlineKeyboardButton(
                    text=button_communal_services, callback_data=cd_communal
                )
            ],
        ]
    )
    return kb


# COMMUNAL_SERVICE: Add counters buttons
def communal_counters_add_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_write_to_db, callback_data=cd_counter_to_db
                )
            ],
            [
                InlineKeyboardButton(
                    text=button_change_counters, callback_data=cd_change_counters
                )
            ],
            [
                InlineKeyboardButton(
                    text=button_communal_services, callback_data=cd_communal
                )
            ],
        ]
    )
    return kb


# COMMUNAL_SERVICE: Back to communal buttons
def communal_back_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_communal_services, callback_data=cd_communal
                )
            ]
        ]
    )
    return kb


# COMMUNAL_SERVICE: Records buttons
def communal_counters_records_buttons(buttons_amount):
    buttons = []
    for i in range(buttons_amount):
        button_text = button_record.format(number=str(i + 1))
        callback = cd_records_buttons_list[i]
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback)])
    buttons.append(
        [InlineKeyboardButton(text=button_communal_services, callback_data=cd_communal)]
    )
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
