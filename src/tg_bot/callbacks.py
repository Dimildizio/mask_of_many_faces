
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


async def create_category_buttons() -> InlineKeyboardMarkup:
    """
    Creates inline keyboard buttons for target categories and put them in rows of 2 elements each.
    Dynamically changes buttons.

    :return: InlineKeyboardMarkup containing the category buttons.
    """
    row, keyboard_buttons = [], []
    for category in ['race', 'class', 'hair', 'beard', 'gender', 'background']:
        text = category.capitalize()
        data = f'menu_{category}'
        row.append(InlineKeyboardButton(text=text, callback_data=data))
        if len(row) == 2:
            keyboard_buttons.append(row)
            row = []
    if row:
        keyboard_buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def main_menu(message: Message) -> None:
    """
    This func creates main menu for character categories

    :param message: message with user info
    :return: None
    """
    keyboard = await create_category_buttons()
    await message.answer('Choose your Character', reply_markup=keyboard)


async def button_callback_handler(query: CallbackQuery) -> None:
    """
    Handles button callbacks from inline keyboards. Categories, subcategories and back button.

    :param query: CallbackQuery.
    :return: None
    """
    match query.data:
        case data if data.startswith('menu_'):  # Check if the callback data starts with 'c_'
            category = data.split('_')[1]
            print('submenu:', category)  # placeholder
        case'back':  # for subcategories to return to main menu
            keyboard = await create_category_buttons()
            await query.message.edit_text("Choose you character", reply_markup=keyboard)
        case _:
            print('Weird case')
