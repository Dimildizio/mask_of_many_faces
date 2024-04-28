from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from src.tg_bot.process_requests import submenu_chosen


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



async def go_to_main(query):
    keyboard = await create_category_buttons()
    await query.message.edit_text("Choose you character", reply_markup=keyboard)


async def create_subcategory_buttons(category: str) -> InlineKeyboardMarkup:
    """
    Creates inline keyboard buttons for subcategories based on the selected category.

    :param category: The main category selected by the user.
    :return: InlineKeyboardMarkup containing the subcategory buttons.
    """
    subcategories = {
        'race': ['Human', 'Dwarf', 'Halfling', 'Firbolg', 'Elf', 'Half-Elf', 'Half-Orc', 'Dragonborn', 'Tiefling',
                 'Gnome'],
        'class': ['Fighter', 'Wizard', 'Barbarian', 'Thief', 'Cleric', 'Artificer', 'Sorcerer', 'Druid', 'Warlock',
                  'Bard', 'Monk', 'Ranger', 'Paladin'],
        'hair': ['Black', 'Red', 'Blonde', 'No'],
        'beard': ['Yes', 'No'],
        'gender': ['Male', 'Female'],
        'background': ['Tavern', 'Forest', 'Ship', 'Dungeon', 'River Bank', 'City']}

    row, keyboard_buttons = [], []
    for subcategory in subcategories.get(category, []):
        text = subcategory
        data = f'submenu_{category}_{subcategory.lower()}'
        row.append(InlineKeyboardButton(text=text, callback_data=data))
        if len(row) == 2:
            keyboard_buttons.append(row)
            row = []
    if row:
        keyboard_buttons.append(row)
    # Adding a back button to go to the main menu
    keyboard_buttons.append([InlineKeyboardButton(text="Back", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def button_callback_handler(query: CallbackQuery) -> None:
    """
    Handles button callbacks from inline keyboards. Categories, subcategories and back button.

    :param query: CallbackQuery.
    :return: None
    """
    await query.answer() # to stop the button from flashing
    match query.data:
        case data if data.startswith('menu_'):  # Check if the callback data starts with 'c_'
            category = data.split('_')[1]
            keyboard = await create_subcategory_buttons(category)
            await query.message.edit_text(f"Choose your {category.title()}", reply_markup=keyboard)

        case data if data.startswith('submenu_'):
            await submenu_chosen(query)
            await go_to_main(query)
        case'back':  # for subcategories to return to main menu
            await go_to_main(query)
        case _:
            print('Weird case')


