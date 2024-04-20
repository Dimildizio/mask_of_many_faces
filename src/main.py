import asyncio
import os

from aiogram import Bot, Dispatcher
from typing import Any

from constants import FACE_DIR, TOKEN
from generation.chargen import generate_image
from swapper.swap_requests import send_image_to_swapper
from tg_bot.handlers import setup_handlers


async def main1():
    character = {'race': 'dwarf', 'dnd_class': 'thief', 'background': 'dungeon', 'hair': 'red', 'beard': True}

    source_img = os.path.join(FACE_DIR, 'peter.png')  # test face
    target_img = generate_image(character)  # test body
    face_path = await send_image_to_swapper(source_img, target_img)
    print(face_path)


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
