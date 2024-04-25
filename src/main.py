import asyncio

from aiogram import Bot, Dispatcher
from typing import Any

from src.utilities.constants import TOKEN
from src.tg_bot.handlers import setup_handlers
from src.database.user_db import create_tables



async def main(disp: Any, io_bot: Any) -> None:
    """
    Starts the polling process for the bot.

    :param disp: Dispatcher for handling updates.
    :param io_bot: The IO-bound operations bot.
    :return: None
    """
    #await create_tables()
    setup_handlers(disp, TOKEN)
    await disp.start_polling(io_bot)


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    asyncio.run(main(dp, bot))
