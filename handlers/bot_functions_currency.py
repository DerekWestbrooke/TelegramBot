from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from handlers.bot_functions_common import show_status_typing
from parsers.api_currency import get_exchange_rates
from resources.bot_keyboards import *
from resources.states import *
from resources.user_logger import create_local_logger

router = Router()
user_logger = create_local_logger()


# Функция возврата к разделу валюты
@router.callback_query(F.data == cd_currency)
async def back_to_currency_main_menu(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == cd_currency:
        await show_status_typing(callback.bot, callback.message.chat.id)
        await callback.message.answer(
            text=message_select_currency_activity,
            reply_markup=currency_action_buttons(),
        )
        await state.set_state(CurrencyBranch.currency_activity)
        await state.clear()
        user_logger.info(f"ВЫБОР ТЕМЫ: валюта (user: {callback.from_user.id})")
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"ВЫБОР ТЕМЫ: неверный ввод (user: {callback.from_user.id})"
        )


# Функция выбора действий в разделе валюты
@router.callback_query(F.data.in_([cd_exchange_rate, cd_calculator]))
async def select_currency_activities(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data in [cd_exchange_rate, cd_calculator]:
        rates_dict = get_exchange_rates()
        rates_dict["BYN"] = ("🇧🇾", "Беларусь", "Белорусский рубль", "1", "1")
        rates = str()
        for key, value in rates_dict.items():
            rates += f"{value[0]} {key} — {value[2]}: {value[3]} (за {value[4]} ед.)\n"
        await state.update_data(rates=rates_dict)
        if callback.data == cd_exchange_rate:
            await callback.message.answer(
                text=message_exchange_rates + rates,
                reply_markup=currency_main_menu_button(),
            )
            user_logger.info(f"КУРС ВАЛЮТ: результат (user: {callback.from_user.id})")
        elif callback.data == cd_calculator:
            await callback.message.answer(
                text=message_input_currency_from,
                reply_markup=currency_main_menu_button(),
            )
            await state.set_state(CurrencyBranch.currency_activity_calculator)
            user_logger.info(
                f"КАЛЬКУЛЯТОР ВАЛЮТ: ввод исходной валюты (user: {callback.from_user.id})"
            )
        else:
            await callback.message.answer(text=message_invalid_input_text)
            user_logger.warning(
                f"ВАЛЮТА: неверный ввод (user: {callback.from_user.id})"
            )


# Функция выбора калькулятора валют
@router.message(CurrencyBranch.currency_activity_calculator)
async def select_currency_from(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    if message.text in currency_info.keys():
        await state.update_data(from_currency=message.text)
        await message.answer(
            text=message_input_currency_to, reply_markup=currency_main_menu_button()
        )
        await state.set_state(CurrencyBranch.currency_activity_calculator_from)
        user_logger.info(
            f"КАЛЬКУЛЯТОР ВАЛЮТ: ввод целевой валюты (user: {message.from_user.id})"
        )
    else:
        await message.answer(text=message_invalid_currency)
        user_logger.warning(
            f"КАЛЬКУЛЯТОР ВАЛЮТ: неверный ввод исходной валюты (user: {message.from_user.id})"
        )


# Функция выбора исходной валюты для калькулятора валют
@router.message(CurrencyBranch.currency_activity_calculator_from)
async def select_currency_to(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    if message.text in currency_info.keys():
        await state.update_data(to_currency=message.text)
        await message.answer(
            text=message_input_amount, reply_markup=currency_main_menu_button()
        )
        await state.set_state(CurrencyBranch.currency_activity_calculator_from_to)
        user_logger.info(
            f"КАЛЬКУЛЯТОР ВАЛЮТ: ввод суммы (user: {message.from_user.id})"
        )
    else:
        await message.answer(text=message_invalid_currency)
        user_logger.info(
            f"КАЛЬКУЛЯТОР ВАЛЮТ: неверный ввод целевой валюты (user: {message.from_user.id})"
        )


# Функция выбора конечной валюты для калькулятора валют
@router.message(CurrencyBranch.currency_activity_calculator_from_to)
async def select_currency_to(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    if message.text.isdecimal():
        data = await state.get_data()
        to_currency = data.get("to_currency")
        from_currency = data.get("from_currency")
        rates_dict = data.get("rates")
        byn_amount = (
            float(message.text) * float(rates_dict[from_currency][3])
        ) / float(rates_dict[from_currency][4])
        result = (byn_amount * float(rates_dict[to_currency][4])) / float(
            rates_dict[to_currency][3]
        )
        await message.answer(
            text=message_convert_result
            + from_currency
            + " "
            + rates_dict[from_currency][0]
            + " "
            + message.text
            + "    "
            + "🔄"
            + "    "
            + to_currency
            + " "
            + rates_dict[to_currency][0]
            + " "
            + str(round(result, 2)),
            reply_markup=currency_main_menu_button(),
        )
        await state.set_state(
            CurrencyBranch.currency_activity_calculator_from_to_amount
        )
        user_logger.info(f"КАЛЬКУЛЯТОР ВАЛЮТ: результат (user: {message.from_user.id})")
    else:
        await message.answer(text=message_invalid_amount)
        user_logger.warning(
            f"КАЛЬКУЛЯТОР ВАЛЮТ: неверный ввод суммы (user: {message.from_user.id})"
        )
