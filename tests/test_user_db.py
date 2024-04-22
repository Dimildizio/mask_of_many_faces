import asyncio
import unittest
from unittest.mock import patch
from src.database.user_db import add_user, fetch_user_data, fetch_user_details, create_tables, update_attr


class TestUserDB(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Ensure that tables are created before running the tests
        await create_tables()

    async def test_add_user(self):
        # Test adding a user and ensure default settings are correctly applied
        user = await add_user(1, 'John', 'Doe', 'Johnny')
        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.user_name, 'John')
        self.assertEqual(user.user_surname, 'Doe')
        self.assertEqual(user.user_nickname, 'Johnny')
        self.assertEqual(user.gender, False)
        # Check default D&D settings
        self.assertEqual(user.race, 'dwarf')
        self.assertEqual(user.hair, 'black')
        self.assertIsNone(user.current_face_image)  # Initially should be None

    async def test_fetch_user_data(self):
        # Test fetching user data
        await add_user(2, 'Jane', 'Smith')
        await fetch_user_data(2)

    async def test_fetch_user_details(self):
        # Test fetching user details, including image paths
        await add_user(3, 'Bob', 'Builder')
        await fetch_user_details(3)

    async def test_update_dnd_attr(self):
        # Test updating a D&D attribute
        await add_user(4, 'Alice', 'Wonderland')
        await update_attr(4, 'dnd_class', 'rogue')
        dnd = await fetch_user_details(4)
        self.assertEqual(dnd.dnd_class, 'rogue')

    async def test_update_image_paths(self):
        # Test updating image paths with fake addresses
        await add_user(5, 'Eve', 'Johnson')
        fake_address = 'fake_image_address.jpg'
        await update_attr(5, 'current_face_image', fake_address)
        user_details = await fetch_user_details(5)
        self.assertEqual(user_details.current_face_image, fake_address)


if __name__ == '__main__':
    unittest.main()
