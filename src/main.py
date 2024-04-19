import asyncio
import os

from constants import FOLDER
from generation.chargen import generate_image
from swapper.swap_requests import send_image_to_swapper


async def main():
    character = {'race': 'dwarf', 'dnd_class': 'thief', 'background': 'dungeon', 'hair': 'red', 'beard': True}

    source_img = os.path.join(FOLDER, 'img_735850.png')  # test
    target_img = generate_image(character)
    face_path = await send_image_to_swapper(source_img, target_img)
    print(face_path)

if __name__ == '__main__':
    asyncio.run(main())
