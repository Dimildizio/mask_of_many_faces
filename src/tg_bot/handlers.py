from aiogram import F
from aiogram.filters.command import Command
from aiogram.types import Message
from datetime import datetime
from typing import Any

from src.constants import SENT_TIME, DELAY_BETWEEN_IMAGES
from src.tg_bot.process_requests import user2db, process_user_face
from src.database.user_db import create_tables


async def prevent_multisending(message: Message) -> bool:
    """
    Prevents multiple messages from being sent in a short time.

    :param message: The message object.
    :return: True if the message can be sent, False otherwise.
    """
    dt = datetime.now()
    last_sent = SENT_TIME.get(message.from_user.id, None)
    if last_sent is None or (dt - last_sent).total_seconds() >= DELAY_BETWEEN_IMAGES:
        SENT_TIME[message.from_user.id] = dt
        return True
    return False


async def handle_start(message: Message) -> None:
    """
    Handles the start command
    :param message: The message with user data.
    :return: None
    """
    await create_tables()
    await user2db(message)
    await message.answer('send a photo, choose settings and type /generate')


async def handle_help(message: Message) -> None:
    """
    Sends a help message to the user with available commands.

    :param message: The user data message from the user.
    :return: None
    """
    await message.answer('send a photo, choose settings from menu and type /generate')


async def handle_contacts(message) -> None:
    """
    Sends the contact information to user.

    :param message: The user data message.
    :return: None
    """
    await message.answer('Ask here @Adjuface_bot and @oaiohmy')


async def handle_image(message, photo: bool) -> None:
    """
    Sends the contact information to user.

    :param message: The user data message.
    :param photo: Image from gallery or as document
    :return: None
    """
    user = await process_user_face(message, photo)


async def handle_unsupported_content(message: Message) -> None:
    """
    Handles all other unsupported content by providing a response to the user.

    :param message: The message with user data.
    :return: None
    """

    await message.answer('No way')


def setup_handlers(dp: Any, bot_token: str) -> None:
    """
    Sets up handlers for different commands, messages, and callbacks.

    :param dp: The bot dispatcher object.
    :param bot_token: The Telegram bot token.
    :return: None
    """
    dp.message(Command('start'))(handle_start)
    dp.message(Command('help'))(handle_help)
    dp.message(Command('contacts'))(handle_contacts)

    #  dp.message(Command('menu'))(handle_category_command)
    #  dp.callback_query()(button_callback_handler)
    async def generic_handler(func, message: Message, photo: bool) -> None:
        if await prevent_multisending(message):
            await func(message, photo)
            return
        await message.answer('too_fast')

    async def image_handler(message: Message) -> None:
        await generic_handler(handle_image, message, True)

    async def doc_handler(message: Message) -> None:
        for ext in [".png", ".jpg", ".jpeg"]:
            if ext in message.document.file_name:
                return await generic_handler(handle_image, message, False)

    dp.message(F.photo)(image_handler)
    dp.message(F.document)(doc_handler)

    dp.message(F.sticker | F.audio | F.video | F.audio | F.poll | F.contact | F.video_note)(
               handle_unsupported_content)
