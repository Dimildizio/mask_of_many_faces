import unittest
from unittest.mock import patch, mock_open

from src.generation.chargen import generate_image
from src.generation.gen_write import write_image
from src.generation.gen_requests import requests_adapter

from tests.constants_for_test import TEST_GEN_FILE, TEST_FAKE_FILEPATH


class TestChargen(unittest.TestCase):
    @patch('src.generation.chargen.get_prompts')
    @patch('src.generation.chargen.requests_adapter')
    @patch('src.generation.chargen.write_image')
    def test_generate_image(self, mock_write_image, mock_requests_adapter, mock_get_prompts):
        mock_get_prompts.return_value = ("prompt", "negative_prompt")
        mock_requests_adapter.return_value = {"output": {"choices": [{"image_base64": "base64string"}]}}
        mock_write_image.return_value = TEST_GEN_FILE

        character = {'race': 'dwarf', 'dnd_class': 'thief', 'background': 'dungeon', 'hair': 'red', 'beard': True}
        result = generate_image(character)
        self.assertEqual(result, TEST_GEN_FILE)
        mock_get_prompts.assert_called_once_with(character)
        mock_requests_adapter.assert_called_once_with("prompt", "negative_prompt")
        mock_write_image.assert_called_once()


class TestGenWrite(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.generation.gen_write.gen_filename')
    def test_write_image(self, mock_gen_filename, mock_file):

        mock_gen_filename.return_value = TEST_FAKE_FILEPATH
        json_image = {"output": {"choices": [{"image_base64": "YmFzZTY0ZW5jb2RlZA=="}]}}  # base64 for 'base64encoded'
        result = write_image(json_image)
        self.assertEqual(result, TEST_FAKE_FILEPATH)
        mock_file.assert_called_once_with(TEST_FAKE_FILEPATH, "wb")
        handle = mock_file()
        handle.write.assert_called_once()


class TestGenRequests(unittest.TestCase):
    @patch('src.generation.gen_requests.send_requests')
    @patch('src.generation.gen_requests.create_request')
    def test_requests_adapter(self, mock_create_request, mock_send_requests):
        mock_create_request.return_value = ({'payload': 'data'}, {'headers': 'info'})
        mock_send_requests.return_value = {'image': 'data'}
        result = requests_adapter("prompt", "negative_prompt")
        self.assertEqual(result, {'image': 'data'})
        mock_create_request.assert_called_once_with("prompt", "negative_prompt")
        mock_send_requests.assert_called_once_with({'payload': 'data'}, {'headers': 'info'})


if __name__ == '__main__':
    unittest.main()
