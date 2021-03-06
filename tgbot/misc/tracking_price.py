import asyncio

from .parser import citilink
from AssistantPriceBot import db, bot
from tgbot.keyboards.inline import tracking_keyboard


async def sleep_for_check_price():
    await asyncio.sleep(3600)


#the script checks every hour to see if the price has changed
async def check_price():
    while True:
        data = await db.get_url_price()
        for i in data:
            name_product, now_price = await citilink(i[1])
            keyboard = await tracking_keyboard(i[1])
            if now_price != i[3]:
                await bot.send_message(int(i[0]), f'Цена на товар {name_product} изменилась! Была {i[3]} стала {now_price}', reply_markup = keyboard)
                await db.update_price(now_price, i[3], i[4])
        await sleep_for_check_price()
