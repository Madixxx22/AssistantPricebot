from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards.reply import menu


async def user_start(message: Message):
    await message.answer("Привет пользователь. Выбери команду из предложенных и начаинай пользоваться!(/help)", reply_markup=menu)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")