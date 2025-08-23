import asyncio

from aiogram import Dispatcher
from handlers.bot_functions_start import router as start_router
from handlers.bot_functions_estate import router as estate_router
from handlers.bot_functions_currency import router as currency_router
from handlers.bot_function_communal import router as communal_router
from handlers.bot_functions_neural import router as neural_router
from resources.bot import bot, db
from handlers.bot_functions_shedule import start_notifications_monitoring
from resources.bot import storage
from resources.user_logger import setup_logger


# Bot parameters
dp = Dispatcher(storage=storage)
dp.include_router(estate_router)
dp.include_router(currency_router)
dp.include_router(communal_router)
dp.include_router(neural_router)
dp.include_router(start_router)


async def main():
    setup_logger()
    start_notifications_monitoring()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
