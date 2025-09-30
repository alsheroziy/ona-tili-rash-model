import asyncio
import logging

from loader import dp, bot
from handlers import setup_routers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from middlewares import ThrottlingMiddleware, AdminMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)


async def on_startup():
    # Set default commands
    await set_default_commands(bot)
    # Notify admins
    await on_startup_notify(bot)


async def main():
    # Register middlewares
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(AdminMiddleware())

    await on_startup()
    # Register all routers
    dp.include_router(setup_routers())
    # Start polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
