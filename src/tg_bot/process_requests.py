from src.database.user_db import add_user, update_attr, fetch_user_details
from src.tg_bot.img_downloader import handle_download
from src.swapper.swap_requests import send_image_to_swapper
from src.generation.chargen import generate_image


async def user2db(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    surname = message.from_user.last_name
    username = message.from_user.username
    return await add_user(user_id, name, surname, username)


async def character2dict(user):
    if user:
        idict = {key: value for key, value in user.__dict__.items() if not key.startswith('_sa_')}
        print(idict)
        return idict
    return None


async def process_user_generation(character):
    target_img = await generate_image(character)  # test body
    return target_img


async def process_user_face(message, photo):
    user = await user2db(message)
    face_img_path = await handle_download(message, photo)
    db_user = await update_attr(user.user_id, 'current_face_image', face_img_path)
    character = await character2dict(db_user)
    target_face = await process_user_generation(character)
    face_path = await send_image_to_swapper(face_img_path, target_face)
    return face_path


async def generate_character(message):
    user = await user2db(message)
    db_user = await update_attr(user.user_id, 'current_target_image', '')
    character = await character2dict(db_user)
    target_face = await process_user_generation(character)
    return target_face


async def process_subcats(query):
    _, category, subcategory = query.data.split('_')
    category = 'dnd_class' if category == 'class' else category
    if category == 'beard':
        subcategory = True if subcategory == 'yes' else False
    elif category == 'gender':
        subcategory = True if subcategory == 'male' else False
    return category, subcategory


async def userdata_output(user_id):
    user_details = await fetch_user_details(user_id)
    character = (f"\nClass: {user_details.dnd_class}"
                 f"\nRace: {user_details.race}"
                 f"\nGender: {'male' if user_details.gender else 'female'}"
                 f"\nBeard: {'yes' if user_details.beard else 'no'}"
                 f"\nHair: {user_details.hair}"
                 f"\nBackground: {user_details.background}")
    return character


async def submenu_chosen(query):
    user_id = query.from_user.id
    category, subcategory = await process_subcats(query)
    await update_attr(user_id, category, subcategory)
    await query.message.answer(f'Character {category} changed to {subcategory}\n')


async def show_character_details(message):
    text = await userdata_output(message.from_user.id)
    await message.answer(f'Current character:\n{text}')
