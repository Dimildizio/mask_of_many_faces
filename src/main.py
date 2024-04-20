import asyncio
import os

from aiogram import Bot, Dispatcher
from typing import Any

from constants import GEN_FOLDER, TOKEN
from generation.chargen import generate_image
from swapper.swap_requests import send_image_to_swapper
from tg_bot.handlers import setup_handlers

async def main1():
    character = {'race': 'dwarf', 'dnd_class': 'thief', 'background': 'dungeon', 'hair': 'red', 'beard': True}

    source_img = os.path.join(GEN_FOLDER, 'img_735850.png')  # test
    target_img = generate_image(character)
    face_path = await send_image_to_swapper(source_img, target_img)
    print(face_path)



async def main(dp: Any, io_bot: Any) -> None:
    """
    Starts the polling process for the bot.

    :param dp: Dispatcher for handling updates.
    :param io_bot: The IO-bound operations bot.
    :return: None
    """
    setup_handlers(dp, TOKEN)
    await dp.start_polling(io_bot)


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    asyncio.run(main(dp, bot))
