import asyncio

from aiogram import Bot, Dispatcher
from typing import Any

from constants import TOKEN
from tg_bot.handlers import setup_handlers



async def main(disp: Any, io_bot: Any) -> None:
    """
    Starts the polling process for the bot.

    :param disp: Dispatcher for handling updates.
    :param io_bot: The IO-bound operations bot.
    :return: None
    """
    setup_handlers(disp, TOKEN)
    await disp.start_polling(io_bot)


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    asyncio.run(main(dp, bot))
