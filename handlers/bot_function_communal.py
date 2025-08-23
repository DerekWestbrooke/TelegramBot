import re

from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from handlers.bot_functions_common import parse_notify_datetime
from handlers.bot_functions_common import show_status_typing
from resources.bot_keyboards import *
from resources.states import *
from resources.values import regex_notify
from resources.bot import db
from resources.user_logger import create_local_logger

router = Router()
user_logger = create_local_logger()


# Обработка кнопки, ведущей на главное окно услуг ЖКХ
@router.callback_query(F.data == cd_communal)
async def back_to_currency_main_menu(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == cd_communal:
        await show_status_typing(callback.bot, callback.message.chat.id)
        await callback.message.answer(
            text=message_select_communal, reply_markup=communal_action_buttons()
        )
        await state.clear()
        await state.set_state(CommunalServices.communal_activity)
        user_logger.info(
            f"ВЫБОР ТЕМЫ: коммунальные услуги (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"ВЫБОР ТЕМЫ: неверный ввод (user: {callback.from_user.id})"
        )


# Главное меню услуг ЖКХ
@router.callback_query(
    CommunalServices.communal_activity,
    F.data.in_([cd_payment, cd_counters, cd_request]),
)
async def select_communal_activities(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data == cd_payment:
        await callback.message.answer(
            text=message_select_payment, reply_markup=communal_remind_question_buttons()
        )
        await state.set_state(CommunalServices.communal_activity_payment)
        user_logger.info(
            f"НАПОМИНАНИЕ: вкл./выкл. опции (user: {callback.from_user.id})"
        )
    elif callback.data == cd_counters:
        await callback.message.answer(
            text=message_counters, reply_markup=communal_counters_buttons()
        )
        await state.set_state(CommunalServices.communal_activity_counters)
        user_logger.info(f"СЧЕТЧИКИ: выбор действия (user: {callback.from_user.id})")
    elif callback.data == cd_request:
        await callback.message.answer(
            text=message_request_bot, reply_markup=main_menu_button()
        )
        await state.set_state(UserObject.user_object)
        user_logger.info(f"КОНТАКТЫ: результат (user: {callback.from_user.id})")
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"ВЫБОР ТЕМЫ: неверный ввод (user: {callback.from_user.id})"
        )


# Функция выбора оповещения об оплате услуг ЖКХ
@router.callback_query(
    CommunalServices.communal_activity_payment, F.data.in_([cd_yes, cd_communal])
)
async def select_payment(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data == cd_yes:
        await callback.message.answer(
            text=message_select_payment_time_and_days,
            reply_markup=communal_main_menu_button(),
        )
        await state.set_state(CommunalServices.communal_activity_payment_time)
        user_logger.info(
            f"НАПОМИНАНИЕ: положительный выбор (user: {callback.from_user.id})"
        )
    elif callback.data == cd_communal:
        await callback.message.answer(text=message_select_no)
        await callback.message.answer(
            text=message_select_type, reply_markup=select_theme_buttons()
        )
        await state.set_state(UserObject.user_object)
        user_logger.info(
            f"НАПОМИНАНИЕ: отрицательный выбор (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"НАПОМИНАНИЕ: неверный ввод выбора (user: {callback.from_user.id})"
        )


# Функция задания времени для получения оповещения пользователем
@router.message(CommunalServices.communal_activity_payment_time)
async def select_payment_input_time(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    if re.fullmatch(regex_notify, message.text, flags=re.IGNORECASE):
        result_times = tuple(
            i.replace(microsecond=0) for i in parse_notify_datetime(message.text)
        )
        if result_times is not None:
            db.insert_notify((message.chat.id, *result_times))
        await message.answer(
            text=message_select_payment_time_and_days_ok,
            reply_markup=communal_main_menu_button(),
        )
        await state.set_state(UserObject.user_object)
        user_logger.info(
            f"НАПОМИНАНИЕ: задание даты и времени для оповещения (user: {message.from_user.id})"
        )
    else:
        user_logger.warning(
            f"НАПОМИНАНИЕ: неверный ввод даты и времени для оповещения (user: {message.from_user.id})"
        )


# Функция выбора действий с показателями счетчиков
@router.callback_query(
    CommunalServices.communal_activity_counters,
    F.data.in_([cd_show_counter, cd_add_counter, cd_delete_counter]),
)
async def select_counters(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    counters = db.select_counters(callback.from_user.id)
    if callback.data == cd_show_counter:
        await callback.message.answer(text=message_show_counters)
        if counters:
            for i in range(len(counters)):
                await callback.message.answer(
                    text=message_pattern_counter_record.format(
                        number=i + 1,
                        electricity=counters[i].electricity,
                        warm_water=counters[i].warm_water,
                        cold_water=counters[i].cold_water,
                    )
                )
            await callback.message.answer(
                text=message_that_is_all, reply_markup=communal_main_menu_button()
            )
        else:
            await callback.message.answer(
                text=message_no_data, reply_markup=communal_main_menu_button()
            )
        await state.set_state(UserObject.user_object)
        user_logger.info(
            f"СЧЕТЧИКИ: результат отображения показаний счетчиков (user: {callback.from_user.id})"
        )
    elif callback.data == cd_add_counter:
        await callback.message.answer(
            text=message_input_counters, reply_markup=communal_main_menu_button()
        )
        await state.set_state(CommunalServices.communal_activity_counters_add)
        user_logger.info(
            f"СЧЕТЧИКИ: ввод новых показателей счетчиков (user: {callback.from_user.id})"
        )
    elif callback.data == cd_delete_counter:
        if counters:
            await callback.message.answer(text=message_show_counters)
            if counters:
                for i in range(len(counters)):
                    await callback.message.answer(
                        text=message_pattern_counter_record.format(
                            number=i + 1,
                            electricity=counters[i].electricity,
                            warm_water=counters[i].warm_water,
                            cold_water=counters[i].cold_water,
                        )
                    )
                await callback.message.answer(
                    text=message_delete_counter,
                    reply_markup=communal_counters_records_buttons(len(counters)),
                )
                await state.set_state(
                    CommunalServices.communal_activity_counters_delete
                )
                user_logger.info(
                    f"СЧЕТЧИКИ: удаление выбранных счетчиков (user: {callback.from_user.id})"
                )

        else:
            await callback.message.answer(
                text=message_no_data, reply_markup=communal_main_menu_button()
            )
            await state.set_state(UserObject.user_object)
            user_logger.info(
                f"СЧЕТЧИКИ: нет счетчиков для удаления (user: {callback.from_user.id})"
            )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"СЧЕТЧИКИ: неверный ввод действий (user: {callback.from_user.id})"
        )


# Функция выбора добавления показателей счетчиков в БД
@router.message(CommunalServices.communal_activity_counters_add)
async def select_payment_input_time(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    m = re.fullmatch(regex_counters, message.text)
    if m:
        electricity = m.group(1)
        warm_water = m.group(2)
        cold_water = m.group(3)
        await state.update_data(electricity=electricity)
        await state.update_data(warm_water=warm_water)
        await state.update_data(cold_water=cold_water)
        await message.answer(
            text=message_input_counters_result.format(
                electricity=electricity, warm_water=warm_water, cold_water=cold_water
            ),
            reply_markup=communal_counters_add_buttons(),
        )
        await state.set_state(CommunalServices.communal_activity_counters_add_question)
        user_logger.info(
            f"СЧЕТЧИКИ: изменение введенных счетчиков (user: {message.from_user.id})"
        )
    else:
        await message.answer(text=message_invalid_payment_time)
        user_logger.warning(
            f"СЧЕТЧИКИ: неверный ввод счетчиков (user: {message.from_user.id})"
        )


# Функция сохранения или изменения показателей счетчиков
@router.callback_query(
    CommunalServices.communal_activity_counters_add_question,
    F.data.in_([cd_counter_to_db, cd_change_counters]),
)
async def select_payment_input_time(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data == cd_counter_to_db:
        data = await state.get_data()
        electricity = data.get("electricity")
        warm_water = data.get("warm_water")
        cold_water = data.get("cold_water")
        db.insert_into_counters(
            (callback.from_user.id, electricity, warm_water, cold_water)
        )
        await callback.message.answer(
            text=message_input_counters_success,
            reply_markup=communal_main_menu_button(),
        )
        await state.set_state(UserObject.user_object)
        user_logger.info(
            f"СЧЕТЧИКИ: сохранение новых счетчиков в БД (user: {callback.from_user.id})"
        )
    elif callback.data == cd_change_counters:
        await callback.message.answer(
            text=message_input_counters, reply_markup=communal_main_menu_button()
        )
        await state.set_state(CommunalServices.communal_activity_counters_add)
        user_logger.info(
            f"СЧЕТЧИКИ: изменение новых счетчиков (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_unknown_text)
        user_logger.warning(
            f"СЧЕТЧИКИ: неверный ввод перед сохранением новых счетчиков (user: {callback.from_user.id})"
        )


# Функция удаления показателей счетчиков из БД
@router.callback_query(
    CommunalServices.communal_activity_counters_delete,
    F.data.in_(cd_records_buttons_list),
)
async def select_counters_delete(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    counters = db.select_counters(callback.from_user.id)
    if callback.data in cd_records_buttons_list:
        counter_to_delete = counters[cd_records_buttons_list.index(callback.data)]
        data_to_delete = (
            counter_to_delete.electricity,
            counter_to_delete.warm_water,
            counter_to_delete.cold_water,
        )
        db.delete_from_counters((callback.from_user.id, *data_to_delete))
        await callback.message.answer(
            text=message_delete_counters_success,
            reply_markup=communal_main_menu_button(),
        )
        await state.set_state(UserObject.user_object)
        user_logger.info(
            f"СЧЕТЧИКИ: удаление выбранных счетчиков (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"СЧЕТЧИКИ: неверный ввод перед удалением выбранных счетчиков (user: {callback.from_user.id})"
        )
