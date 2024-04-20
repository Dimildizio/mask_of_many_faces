import asyncio
import unittest
from src.database.user_db import add_user, fetch_user_data, fetch_user_details, create_tables


class TestUserDB(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Ensure that tables are created before running the tests
        await create_tables()

    async def test_add_user(self):
        # Test adding a user
        user_id = await add_user(1, 'John', 'Doe', 'Johnny')
        self.assertIsNotNone(user_id)

    async def test_fetch_user_data(self):
        # Test fetching user data
        await add_user(2, 'Jane', 'Smith')
        await fetch_user_data(2)  # This should print user data

    async def test_fetch_user_details(self):
        # Test fetching user details
        await add_user(3, 'Bob', 'Builder')
        await fetch_user_details(3)  # This should print user details

if __name__ == '__main__':
    unittest.main()
