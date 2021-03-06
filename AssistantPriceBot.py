from aiogram import Dispatcher, Bot
from aiogram.dispatcher import storage

from tgbot.config import load_config
from tgbot.models.postgresql import Database

#create global variables
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
db = Database()
dp = Dispatcher(bot, storage=storage)