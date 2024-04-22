import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from aiogram.types import Message, User, Chat, PhotoSize
from src.tg_bot.process_requests import user2db, process_user_face, change_value
from tests.constants_for_test import TEST_FAKE_FILEPATH

class TestImgDownload(unittest.TestCase):
    @patch('src.tg_bot.img_download.aiohttp.ClientSession')
    async def test_handle_download(self, mock_session):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b'image_data')

        mock_session.return_value.__aenter__.return_value.get.return_value = mock_response

        from src.tg_bot.img_downloader import handle_download
        message = Message(message_id=123, date=0, chat=Chat(id=0, type='private'),
                          photo=[PhotoSize(file_id='file123', width=100, height=100, file_unique_id='unique_id_value')],
                          from_user=User(id=1, is_bot=False, first_name='test'))

        result = await handle_download(message)
        self.assertEqual(result, 'path_to_downloaded_image.png')


class TestBotCommands(unittest.TestCase):
    @patch('aiogram.types.Message.answer')
    async def test_handle_help(self, mock_answer):
        from src.tg_bot.handlers import handle_help
        message = Message(message_id=123, date=0, chat=Chat(id=0, type='private'),
                          from_user=User(id=1, is_bot=False, first_name='test'))
        await handle_help(message)
        mock_answer.assert_called_once_with('send a photo, choose settings from menu and type /generate')

    @patch('aiogram.types.Message.answer')
    async def test_handle_contacts(self, mock_answer):
        from src.tg_bot.handlers import handle_contacts
        message = Message(message_id=123, date=0, chat=Chat(id=0, type='private'),
                          from_user=User(id=1, is_bot=False, first_name='test'))
        await handle_contacts(message)
        mock_answer.assert_called_once_with('Ask here @Adjuface_bot and @oaiohmy')

    @patch('aiogram.types.Message.answer')
    async def test_handle_unsupported_content(self, mock_answer):
        from src.tg_bot.handlers import handle_unsupported_content
        message = Message(message_id=123, date=0, chat=Chat(id=0, type='private'),
                          from_user=User(id=1, is_bot=False, first_name='test'))
        await handle_unsupported_content(message)
        mock_answer.assert_called_once_with('No way')


class TestHandlers(unittest.TestCase):
    @patch('src.tg_bot.handlers.handle_image')
    async def test_handle_image(self, mock_handle_image):
        mock_handle_image.return_value = TEST_FAKE_FILEPATH

        from src.tg_bot.handlers import handle_image
        message = Message(message_id=123, date=0, chat=Chat(id=0, type='private'),
                          from_user=User(id=1, is_bot=False, first_name='test'))

        result = await handle_image(message, photo=True)
        self.assertEqual(result, TEST_FAKE_FILEPATH)

    @patch('src.tg_bot.handlers.prevent_multisending')
    @patch('src.tg_bot.handlers.handle_start')
    async def test_handle_start_with_rate_limit(self, mock_handle_start, mock_prevent_multisending):
        mock_prevent_multisending.return_value = False
        mock_handle_start.return_value = None

        from src.tg_bot.handlers import handle_start
        message = Message(message_id=123, date=0, chat=Chat(id=0, type='private'),
                          from_user=User(id=1, is_bot=False, first_name='test'))

        await handle_start(message)
        mock_handle_start.assert_not_called()


class TestProcessRequests(unittest.IsolatedAsyncioTestCase):
    async def test_user2db(self):
        # Mocking the message object with a non-None photo attribute
        message = Message(
            message_id=123,
            date=0,
            chat=Chat(id=0, type='private'),
            hoto=[PhotoSize(file_id='file123', width=100, height=100, file_unique_id='unique_id_value')],
            # Ensure photo attribute is not None
            from_user=User(id=123, first_name='John', last_name='Doe', username='johndoe', is_bot=False)
        )
        # Mocking the add_user function
        with patch('src.tg_bot.process_requests.add_user') as mock_add_user:
            mock_add_user.return_value = AsyncMock()  # Mocking the return value of add_user function
            await user2db(message)
            mock_add_user.assert_called_once_with(123, 'John', 'Doe', 'johndoe')

    async def test_change_value(self):
        # Mocking the callback query object with required fields
        query_mock = MagicMock()
        query_mock.from_user = MagicMock(id=123, is_bot=False, first_name='John')
        query_mock.chat_instance = 'chat_instance_value'

        # Mocking the update_attr function
        with patch('src.tg_bot.process_requests.update_attr') as mock_update_attr:
            mock_update_attr.return_value = AsyncMock()
            await change_value(query_mock)


if __name__ == '__main__':
    unittest.main()
