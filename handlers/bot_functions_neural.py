import asyncio

from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.bot_functions_common import show_status_typing
from parsers.api_neural_network import send_user_message_to_neural_network
from resources.bot_keyboards import *
from resources.states import *
from resources.user_logger import create_local_logger

router = Router()
user_logger = create_local_logger()


# Функция выбора общения с нейросетью
@router.message(NeuralNetwork.neural_question)
async def question_for_neural_network(message: types.Message, state: FSMContext):
    await show_status_typing(message.bot, message.chat.id)
    if isinstance(message.text, str):
        await message.answer(text=message_neural_wait)
        answer = await asyncio.to_thread(
            send_user_message_to_neural_network, message.text
        )
        if answer == message_neural_network_not_found:
            await message.answer(
                text=message_neural_network_not_found, reply_markup=main_menu_button()
            )
            user_logger.info(
                f"НЕЙРОСЕТЬ С API: нет ответа (user: {message.from_user.id})"
            )
        else:
            await message.answer(
                text=message_neural_network_answer + '"' + answer + '"',
                reply_markup=main_menu_button(),
            )
            user_logger.info(
                f"НЕЙРОСЕТЬ С API: ответ пользователю (user: {message.from_user.id})"
            )
        await state.set_state(UserObject.user_object)
