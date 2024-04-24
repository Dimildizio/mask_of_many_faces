from src.database.user_db import add_user, update_attr
from src.tg_bot.img_downloader import handle_download
from src.swapper.swap_requests import send_image_to_swapper
from src.generation.chargen import generate_image

async def user2db(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    surname = message.from_user.last_name
    username = message.from_user.username
    return await add_user(user_id, name, surname, username)


async def process_user_face(message, photo):
    user = await user2db(message)
    face_img_path = await handle_download(message, photo)
    db_user = await update_attr(user.user_id, 'current_face_image', face_img_path)
    target_face = await process_user_generation(db_user.character)
    face_path = await send_image_to_swapper(face_img_path, target_face)
    return face_path


async def process_user_generation(character):
    target_img = await generate_image(character)  # test body
    return target_img


async def change_value(query) -> None:
    """
    Processes the selection of a button to change attribute.

    :param query: The callback query.
    :return: None

    """
    user_id = query.from_user.id
    attribute, value = query.data[0], query.data[1]
    updated = await update_attr(user_id, attribute, value)
    if updated:
        print(f'{user_id} user {attribute} updated to {value}')

