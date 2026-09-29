import asyncio

from maxapi import Dispatcher
from maxapi.context import RedisContext

from config import bot, redis_client
from functions.maxapi_patch import MediaCache
from functions.smart_answer_func import apply_patch
from handlers.chapter1 import chapter1
from handlers.last_stand import last_stand
from handlers.introduction import introduction
from handlers.menu import menu
from logger import get_logger, setup_logging
from middlewares.logger_middleware import BotMiddleware

setup_logging()
log = get_logger()

async def main():
    dp = Dispatcher(
        storage=RedisContext,
        redis_client=redis_client,
        key_prefix="maxwater"
    )

    dp.register_outer_middleware(BotMiddleware())
    dp.include_routers(
        introduction,
        menu,
        chapter1,
        last_stand
    )

    try:
        MediaCache.load()
        apply_patch()

        log.info("🚀 Bot starting")

        await dp.start_polling(bot)

    except Exception:
        log.exception("🆘 Bot crashed")

    finally:
        await bot.close_session()


if __name__ == "__main__":
    asyncio.run(main())