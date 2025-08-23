import html

from aiogram import Router
from aiogram import types, F
from aiogram.filters import (
    Command,
    CommandStart,
)
from aiogram.fsm.context import FSMContext

from handlers.bot_functions_common import show_status_typing
from parsers.api_neural_network import is_api_exist
from resources.bot import db
from resources.bot_keyboards import *
from resources.states import *
from resources.user_logger import create_local_logger

router = Router()
user_logger = create_local_logger()


# Функция входа пользователя в чат с ботом
@router.callback_query(F.data == cd_start_bot)
async def start_bot(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data == cd_start_bot:
        db.insert_user(
            (
                callback.from_user.id,
                callback.from_user.username,
                callback.message.chat.id,
            )
        )
        await callback.message.answer(
            text=message_select_type, reply_markup=select_theme_buttons()
        )
        await state.set_state(UserObject.user_object)
        user_logger.info(
            f"ГЛАВНОЕ МЕНЮ: выбор темы для общения (user: {callback.from_user.id})"
        )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"СТАРТ БОТА: неверный ввод (user: {callback.from_user.id})"
        )


# Выбор темы для общения
@router.callback_query(
    UserObject.user_object,
    F.data.in_([cd_estate, cd_currency, cd_communal, cd_neural_network]),
)
async def select_object(callback: types.CallbackQuery, state: FSMContext):
    await show_status_typing(callback.bot, callback.message.chat.id)
    if callback.data == cd_estate:
        await callback.message.answer(
            text=message_estate_action, reply_markup=estate_activity_buttons()
        )
        await state.set_state(EstateBranch.estate_activity)
        user_logger.info(f"ВЫБОР ТЕМЫ: недвижимость (user: {callback.from_user.id})")
    elif callback.data == cd_currency:
        await callback.message.answer(
            text=message_select_currency_activity,
            reply_markup=currency_action_buttons(),
        )
        await state.set_state(CurrencyBranch.currency_activity)
        user_logger.info(f"ВЫБОР ТЕМЫ: валюта (user: {callback.from_user.id})")
    elif callback.data == cd_communal:
        await callback.message.answer(
            text=message_select_communal, reply_markup=communal_action_buttons()
        )
        await state.set_state(CommunalServices.communal_activity)
        user_logger.info(
            f"ВЫБОР ТЕМЫ: коммунальные услуги (user: {callback.from_user.id})"
        )
    elif callback.data == cd_neural_network:
        if is_api_exist():
            await callback.message.answer(
                text=message_neural_network, reply_markup=main_menu_button()
            )
            await state.set_state(NeuralNetwork.neural_question)
            user_logger.info(
                f"ВЫБОР ТЕМЫ: нейросеть c API (user: {callback.from_user.id})"
            )
        else:
            await callback.message.answer(
                text=message_api_is_none, reply_markup=main_menu_button()
            )
            user_logger.info(
                f"ВЫБОР ТЕМЫ: нейросеть без API (user: {callback.from_user.id})"
            )
    else:
        await callback.message.answer(text=message_invalid_input_text)
        user_logger.warning(
            f"ВЫБОР ТЕМЫ: неверный ввод (user: {callback.from_user.id})"
        )


# Перезапуск бота
@router.message(Command("restart"))
async def restart_bot(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=message_restart)
    await send_welcome(message, state)
    user_logger.info(f"Перезапуск бота (user: {message.from_user.id})")


# Старт бота
@router.message(CommandStart)
async def welcome_message(message: types.Message, state: FSMContext):
    await send_welcome(message, state)
    user_logger.info(f"Запуск бота (user: {message.from_user.id})")


# Приветствие
async def send_welcome(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    await message.answer(
        f"👋 {html.escape(message.from_user.full_name)}, " + message_greeting,
        reply_markup=start_button(),
    )
    await state.set_state(UserObject.user_entrance)
