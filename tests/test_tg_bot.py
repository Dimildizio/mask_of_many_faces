import unittest
from unittest.mock import patch, AsyncMock
from aiogram.types import Message, User, Chat


class TestImgDownload(unittest.TestCase):
    @patch('src.tg_bot.img_download.aiohttp.ClientSession')
    async def test_handle_download(self, mock_session):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b'image_data')

        mock_session.return_value.__aenter__.return_value.get.return_value = mock_response

        from src.tg_bot.img_downloader import handle_download
        message = Message(message_id=123, date=0, chat=Chat(id=0, type='private'),
                          photo=[type('obj', (object,), {'file_id': 'file123'})],
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
    @patch('src.tg_bot.handlers.handle_download')
    async def test_handle_image(self, mock_handle_download):
        mock_handle_download.return_value = '/fake/path/to/image.png'

        from src.tg_bot.handlers import handle_image
        message = Message(message_id=123, date=0, chat=Chat(id=0, type='private'),
                          from_user=User(id=1, is_bot=False, first_name='test'))

        result = await handle_image(message, photo=True)
        self.assertEqual(result, '/fake/path/to/image.png')

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


if __name__ == '__main__':
    unittest.main()
