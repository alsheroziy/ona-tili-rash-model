from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data import config

# Bot instance with default HTML parse mode
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# FSM storage (in-memory)
storage = MemoryStorage()
# Dispatcher
dp = Dispatcher(storage=storage)
