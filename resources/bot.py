import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from resources.values import API_TOKEN

from parsers.parser_kufar import KufarParser
from resources.database import DataBase
from resources.values import POSTGRES_DB

# Инициализация хранилища
storage = MemoryStorage()

# Инициализация бота
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# Инициализация парсера сайта Kufar
parser_kufar = KufarParser(bot=bot)
# Инициализация
db = DataBase(POSTGRES_DB)
