import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

#import from the current project
from AssistantPriceBot import db
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.delete_products import register_callback_handler
from tgbot.handlers.help import register_help
from tgbot.handlers.url import register_url
from tgbot.handlers.user import register_user
from tgbot.handlers.view_product import register_view_pr
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.AntiFlood import AntiFlood
from tgbot.misc.tracking_price import check_price

logger = logging.getLogger(__name__)

def register_all_middlewares(dp: Dispatcher):
    dp.setup_middleware(DbMiddleware())
    dp.setup_middleware(AntiFlood())


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    register_admin(dp)
    register_user(dp)
    register_view_pr(dp)
    register_help(dp)
    register_url(dp)
    register_callback_handler(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await db.create()
        await db.create_table_users()

        #create thread for tracking_price
        asyncio.ensure_future(check_price())

        #start main thread
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.get_session()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")