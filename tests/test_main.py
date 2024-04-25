import unittest
import os

from src.constants import FACE_DIR
from src.generation.chargen import generate_image
from src.swapper.swap_requests import send_image_to_swapper

class MainTest(unittest.IsolatedAsyncioTestCase):  # Using the appropriate class for async tests

    async def test_image_generation_and_swapping(self, user_file = 'peter.png'):  # Ensure method name starts with 'test'
        character = {'race': 'elf', 'dnd_class': 'paladin', 'background': 'castle', 'hair': 'black', 'beard': True}


        source_img = os.path.join(FACE_DIR, user_file)  # Test face
        target_img = generate_image(character)  # Test body
        face_path = await send_image_to_swapper(source_img, target_img)  # Await the async function
        print(face_path)
        # Send the image to user message.answer_photo(FSInputFile(face_path))

if __name__ == '__main__':
    unittest.main()
