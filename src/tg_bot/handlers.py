from aiogram import F
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile
from datetime import datetime
from typing import Any

from utilities.constants import SENT_TIME, DELAY_BETWEEN_IMAGES
from tg_bot.process_requests import user2db, process_user_face, show_character_details, generate_character
from tg_bot.callbacks import button_callback_handler, main_menu
from database.user_db import create_tables


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
    await message.answer('choose settings and type /generate or send a photo to create a character with your face')


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


async def handle_generate(message):
    char_image = await generate_character(message)
    await message.answer_photo(FSInputFile(char_image))


async def handle_image(message, photo: bool) -> None:
    """
    Sends the contact information to user.

    :param message: The user data message.
    :param photo: Image from gallery or as document
    :return: None
    """
    file_address = await process_user_face(message, photo)
    print(file_address)
    await message.answer_photo(FSInputFile(file_address[0]))


async def handle_unsupported_content(message: Message) -> None:
    """
    Handles all other unsupported content by providing a response to the user.

    :param message: The message with user data.
    :return: None
    """

    await message.answer('No way')


def setup_handlers(dp: Any) -> None:
    """
    Sets up handlers for different commands, messages, and callbacks.

    :param dp: The bot dispatcher object.
    :return: None
    """
    dp.message(Command('start'))(handle_start)
    dp.message(Command('help'))(handle_help)
    dp.message(Command('contacts'))(handle_contacts)
    dp.message(Command('menu'))(main_menu)
    dp.message(Command('character'))(show_character_details)
    dp.message(Command('generate'))(handle_generate)

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

    dp.callback_query()(button_callback_handler)
