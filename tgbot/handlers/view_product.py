from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from AssistantPriceBot import db
from tgbot.keyboards.inline import view_keyboard


#Processor for viewing all user's products
async def view_start(message):
    answer_view = await db.view_product(message.from_user.id)
    auto_number = 1
    for i in answer_view:
        result = str(auto_number) + "." + i[1] + " - " + i[2] + '. Прошлая цена ' + i[3] 
        keyboard = await view_keyboard(i[0])
        await message.answer(result, reply_markup = keyboard)
        auto_number += 1


def register_view_pr(dp: Dispatcher):
    dp.register_message_handler(view_start, commands="view_all_products")
    dp.register_message_handler(view_start, Text(equals="Просмотр товаров"))
