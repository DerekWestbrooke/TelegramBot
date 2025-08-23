import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from parsers.parser_kufar import KufarParser
from resources.database import DataBase
from resources.values import db_name

# Инициализация хранилища
storage = MemoryStorage()
# Выгрузка переменных окружения
load_dotenv()
# Выгрузка токена бота из ранее выгруженных переменных окружения
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация бота
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# Инициализация парсера сайта Kufar
parser_kufar = KufarParser(bot=bot)
# Инициализация
db = DataBase(db_name)
