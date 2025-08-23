import asyncio
from datetime import datetime, timedelta

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from handlers.bot_functions_common import show_status_typing
from handlers.bot_functions_common import (
    sort_locations_list,
    start_searching_site_advs_thread,
)
from resources.bot import db
from resources.bot import parser_kufar
from resources.bot_keyboards import *
from resources.states import *
from resources.user_logger import create_local_logger

router = Router()
user_logger = create_local_logger()


# Функция перехода к действиям раздела недвижимости
@router.callback_query(F.data == cd_estate)
async def back_to_estate_main_menu(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == cd_estate:
        await show_status_typing(callback.bot, callback.message.chat.id)
        await callback.message.answer(
            text=message_estate_action, reply_markup=estate_activity_buttons()
        )
        await state.clear()
        await state.set_state(EstateBranch.estate_activity)
        user_logger.info(f"ВЫБОР ТЕМЫ: недвижимость (user: {callback.from_user.id})")
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"ВЫБОР ТЕМЫ: неверный ввод (user: {callback.from_user.id})"
        )


# Функция выбора сайта
@router.callback_query(EstateBranch.estate_activity, F.data.in_([cd_rent, cd_purchase]))
async def select_site_to_parse(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data == cd_rent:
        await callback.message.answer(
            text=message_estate_site + " для аренды.",
            reply_markup=estate_site_buttons(),
        )
        await state.update_data(activity="Rent")
        await state.set_state(EstateBranch.estate_activity_site)
        user_logger.info(f"НЕДВИЖИМОСТЬ: аренда (user: {callback.from_user.id})")
    elif callback.data == cd_purchase:
        await callback.message.answer(
            text=message_estate_site + " для покупки.",
            reply_markup=estate_site_buttons(),
        )
        await state.update_data(activity="Purchase")
        await state.set_state(EstateBranch.estate_activity_site)
        user_logger.info(f"НЕДВИЖИМОСТЬ: покупка (user: {callback.from_user.id})")
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод формы владения (user: {callback.from_user.id})"
        )


# Функция выбора местоположения
@router.callback_query(EstateBranch.estate_activity_site, F.data == cd_kufar)
async def select_kufar_location(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data == cd_kufar:
        if callback.data == cd_kufar:
            user_logger.info(f"НЕДВИЖИМОСТЬ: Kufar (user: {callback.from_user.id})")
        await callback.message.answer(message_wait_locations)
        if not db.is_table_empty("kufar_locations"):
            metadata = db.select_data_from_table("metadata")
            metadata_dict = dict()
            for item in metadata:
                metadata_dict[item.parameter] = item.value
            if "kufar_last_location_update" in metadata_dict.keys():
                kufar_last_update = datetime.fromisoformat(
                    metadata_dict["kufar_last_location_update"]
                )
            else:
                kufar_last_update = datetime.min

            if datetime.now().replace(microsecond=0) - kufar_last_update <= timedelta(
                days=30
            ):
                locations_from_table = db.select_data_from_table("kufar_locations")
                locations = [item.location_name for item in locations_from_table]
            else:
                locations = parser_kufar.get_locations_names()
                db.delete_values("kufar_locations")
                db.insert_kufar_values(locations)
        else:
            locations = parser_kufar.get_locations_names()
            db.insert_kufar_values(locations)
        await state.update_data(locations=locations)
        await callback.message.answer(
            text=message_location, reply_markup=estate_main_menu_button()
        )
        await state.set_state(EstateBranch.estate_activity_site_location)
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод сайта (user: {callback.from_user.id})"
        )


# Функция выбора валюты
@router.message(EstateBranch.estate_activity_site_location)
async def select_kufar_currency(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    data = await state.get_data()
    locations = data.get("locations")
    if message.text in locations:
        await state.update_data(city=message.text)
        data = await state.get_data()
        if not ("currency" in data or "min_sum" in data or "max_sum" in data):
            await message.answer(
                text=message_enter_currency, reply_markup=estate_currency_buttons()
            )
            await state.set_state(EstateBranch.estate_activity_site_location_currency)
            user_logger.info(
                f"НЕДВИЖИМОСТЬ: задание минимальной стоимости (user: {message.from_user.id})"
            )
        else:
            min_sum = data.get("min_sum")
            max_sum = data.get("max_sum")
            city = data.get("city")
            currency = data.get("currency")
            activity = "аренда" if data.get("activity") == "Rent" else "покупка"
            await message.answer(
                text=message_filter_kufar.format(
                    activity=activity,
                    location=city,
                    currency=currency,
                    min_price=min_sum,
                    max_price=max_sum,
                ),
                reply_markup=estate_kufar_filter_buttons(),
            )
            await state.set_state(
                EstateBranch.estate_activity_site_location_currency_min_max_filter
            )
            user_logger.info(
                f"НЕДВИЖИМОСТЬ: переход к фильтру (user: {message.from_user.id})"
            )
    else:
        await message.answer(text=message_invalid_location)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод местоположения (user: {message.from_user.id})"
        )


# Функция выбора минимальной стоимости для сайта Kufar
@router.callback_query(EstateBranch.estate_activity_site_location_currency)
async def select_kufar_min_cost(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data in cd_currencies:
        await state.update_data(
            currency=buttons_currency[cd_currencies.index(callback.data)]
        )
        await state.update_data(
            currency=buttons_currency[cd_currencies.index(callback.data)]
        )
        data = await state.get_data()
        currency = data.get("currency")
        if not ("min_sum" in data or "max_sum" in data):
            await callback.message.answer(
                text=message_enter_min_cost.format(currency=currency),
                reply_markup=estate_main_menu_button(),
            )
            await state.set_state(
                EstateBranch.estate_activity_site_location_currency_min
            )
            user_logger.info(
                f"НЕДВИЖИМОСТЬ: задание минимальной стоимости (user: {callback.from_user.id})"
            )
        else:
            activity = "аренда" if data.get("activity") == "Rent" else "покупка"
            min_sum = data.get("min_sum")
            max_sum = data.get("max_sum")
            city = data.get("city")
            currency = data.get("currency")
            await callback.message.answer(
                text=message_filter_kufar.format(
                    activity=activity,
                    location=city,
                    currency=currency,
                    min_price=min_sum,
                    max_price=max_sum,
                ),
                reply_markup=estate_kufar_filter_buttons(),
            )
            await state.set_state(
                EstateBranch.estate_activity_site_location_currency_min_max_filter
            )
            user_logger.info(
                f"НЕДВИЖИМОСТЬ: переход к фильтру (user: {callback.from_user.id})"
            )
    else:
        await callback.message.answer(
            text=message_invalid_currency, reply_markup=estate_currency_buttons()
        )
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод валюты (user: {callback.from_user.id})"
        )


# Функция выбора максимальной стоимости
@router.message(EstateBranch.estate_activity_site_location_currency_min)
async def select_kufar_max_cost(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    if message.text.isdecimal():
        await state.update_data(min_sum=message.text)
        data = await state.get_data()
        currency = data.get("currency")
        if not ("max_sum" in data):
            await message.answer(
                text=message_enter_max_cost.format(currency=currency),
                reply_markup=estate_main_menu_button(),
            )
            await state.set_state(
                EstateBranch.estate_activity_site_location_currency_min_max
            )
            user_logger.info(
                f"НЕДВИЖИМОСТЬ: задание минимальной стоимости (user: {message.from_user.id})"
            )
        else:
            if float(message.text) < float(data.get("max_sum")):
                activity = "аренда" if data.get("activity") == "Rent" else "покупка"
                min_sum = data.get("min_sum")
                max_sum = data.get("max_sum")
                city = data.get("city")
                currency = data.get("currency")
                await message.answer(
                    text=message_filter_kufar.format(
                        activity=activity,
                        location=city,
                        currency=currency,
                        min_price=min_sum,
                        max_price=max_sum,
                    ),
                    reply_markup=estate_kufar_filter_buttons(),
                )
                await state.set_state(
                    EstateBranch.estate_activity_site_location_currency_min_max_filter
                )
            elif float(message.text) >= float(data.get("max_sum")):
                await message.answer(text=message_min_more_max)
                user_logger.warning(
                    f"НЕДВИЖИМОСТЬ: неверный ввод минимальной стоимости (user: {message.from_user.id})"
                )
    else:
        await message.answer(message_invalid_min)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод минимальной стоимости (user: {message.from_user.id})"
        )


@router.message(EstateBranch.estate_activity_site_location_currency_min_max)
async def select_kufar_parse(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    data = await state.get_data()
    if message.text.isdecimal() and float(message.text) > float(data.get("min_sum")):
        await state.update_data(max_sum=message.text)
        data = await state.get_data()
        min_sum = data.get("min_sum")
        max_sum = data.get("max_sum")
        city = data.get("city")
        currency = data.get("currency")

        activity = "аренда" if data.get("activity") == "Rent" else "покупка"

        await message.answer(
            text=message_filter_kufar.format(
                activity=activity,
                location=city,
                currency=currency,
                min_price=min_sum,
                max_price=max_sum,
            ),
            reply_markup=estate_kufar_filter_buttons(),
        )

        await state.set_state(
            EstateBranch.estate_activity_site_location_currency_min_max_filter
        )

        user_logger.info(
            f"НЕДВИЖИМОСТЬ: задание максимальной стоимости (user: {message.from_user.id})"
        )
    elif message.text.isdecimal() and float(message.text) <= float(data.get("min_sum")):
        await message.answer(message_max_less_min)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод максимальной стоимости (user: {message.from_user.id})"
        )
    else:
        await message.answer(message_invalid_max)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод максимальной стоимости (user: {message.from_user.id})"
        )


# Функция старта мониторинга
@router.callback_query(F.data == cd_start_parsing)
async def start_kufar_parsing(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == cd_start_parsing:
        chat_id = callback.message.chat.id
        await show_status_typing(callback.bot, callback.message.chat.id)
        data = await state.get_data()
        min_sum = data.get("min_sum")
        max_sum = data.get("max_sum")
        city = data.get("city")
        currency = data.get("currency")
        parser_kufar.activity = data.get("activity", "Rent")
        parser_kufar.chat_id = chat_id
        parser_kufar.loop = asyncio.get_event_loop()
        start_searching_site_advs_thread(parser_kufar, city, min_sum, max_sum, currency)
        await callback.message.answer(
            text=message_start_to_parse, reply_markup=estate_kufar_stop_button()
        )
        await state.set_state(
            EstateBranch.estate_activity_site_location_currency_min_max_filter_parsing
        )
        user_logger.info(
            f"НЕДВИЖИМОСТЬ: запуск мониторинга (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод перед началом мониторинга объявлений (user: {callback.from_user.id})"
        )


# Функция изменения фильтра
@router.callback_query(
    F.data.in_(
        [cd_edit_location, cd_edit_min_price, cd_edit_max_price, cd_edit_currency]
    )
)
async def edit_filter_parameters(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    data = await state.get_data()
    currency = data.get("currency")
    if callback.data == cd_edit_location:
        locations = data.get("locations", [])
        location_string = sort_locations_list(locations)
        await callback.message.answer(
            message_edit_location + location_string,
            reply_markup=estate_main_menu_button(),
        )
        await state.set_state(EstateBranch.estate_activity_site_location)
        await callback.answer()
        user_logger.info(
            f"НЕДВИЖИМОСТЬ: изменение местоположения (user: {callback.from_user.id})"
        )
    elif callback.data == cd_edit_min_price:
        await callback.message.answer(
            text=message_edit_min_cost.format(currency=currency),
            reply_markup=estate_main_menu_button(),
        )
        await state.set_state(EstateBranch.estate_activity_site_location_currency_min)
        await callback.answer()
        user_logger.info(
            f"НЕДВИЖИМОСТЬ: изменение минимальной стоимости (user: {callback.from_user.id})"
        )
    elif callback.data == cd_edit_max_price:
        await callback.message.answer(
            text=message_edit_max_cost.format(currency=currency),
            reply_markup=estate_main_menu_button(),
        )
        await state.set_state(
            EstateBranch.estate_activity_site_location_currency_min_max
        )
        await callback.answer()
        user_logger.info(
            f"НЕДВИЖИМОСТЬ: изменение максимальной стоимости (user: {callback.from_user.id})"
        )
    elif callback.data == cd_edit_currency:
        await callback.message.answer(
            text=message_edit_currency, reply_markup=estate_currency_buttons()
        )
        await state.set_state(EstateBranch.estate_activity_site_location_currency)
        await callback.answer()
        user_logger.info(
            f"НЕДВИЖИМОСТЬ: изменение валюты (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод при изменении фильтра (user: {callback.from_user.id})"
        )


# Функция остановки мониторинга
@router.callback_query(F.data == cd_stop_parsing)
async def stop_kufar_parsing(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == cd_stop_parsing:
        await show_status_typing(callback.bot, callback.message.chat.id)
        parser_kufar.stop_kufar_parsing()
        await callback.message.answer(
            text=message_stop_to_parse, reply_markup=estate_kufar_stop_back_button()
        )
        await state.set_state(
            EstateBranch.estate_activity_site_location_currency_min_max_filter_parsing_stop
        )
        user_logger.info(
            f"НЕДВИЖИМОСТЬ: остановка мониторинга (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод перед остановкой мониторинга (user: {callback.from_user.id})"
        )


# Функция возврата в главное меню
@router.callback_query(F.data == cd_main_menu)
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == cd_main_menu:
        await show_status_typing(callback.bot, callback.message.chat.id)
        await callback.message.answer(
            text=message_select_type, reply_markup=select_theme_buttons()
        )
        await state.set_state(UserObject.user_object)
        user_logger.info(
            f"НЕДВИЖИМОСТЬ: возврат в главное меню (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"ВЫБОР ТЕМЫ: неверный ввод (user: {callback.from_user.id})"
        )


# Функция изменения фильтра
@router.callback_query(F.data == cd_kufar_edit_filter)
async def back_to_kufar_filter(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == cd_kufar_edit_filter:
        await show_status_typing(callback.bot, callback.message.chat.id)
        await state.set_state(
            EstateBranch.estate_activity_site_location_currency_min_max_filter
        )
        data = await state.get_data()
        activity = "аренда" if data.get("activity") == "Rent" else "покупка"
        min_sum = data.get("min_sum")
        max_sum = data.get("max_sum")
        city = data.get("city")
        currency = data.get("currency")
        await callback.message.answer(
            text=message_filter_kufar.format(
                activity=activity,
                location=city,
                currency=currency,
                min_price=min_sum,
                max_price=max_sum,
            ),
            reply_markup=estate_kufar_filter_buttons(),
        )
        await state.clear()
        user_logger.info(
            f"НЕДВИЖИМОСТЬ: изменение фильтра (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"НЕДВИЖИМОСТЬ: неверный ввод при изменении фильтра (user: {callback.from_user.id})"
        )
