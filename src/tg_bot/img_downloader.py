import aiohttp
import io
import os

from PIL import Image

from utilities.constants import TOKEN, FACE_DIR


async def get_file_data(message, photo=True):
    file_id = message.photo[-1].file_id if photo else message.document.file_id
    file_info = await message.bot.get_file(file_id)

    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    input_path = os.path.join(FACE_DIR, f"{file_info.file_unique_id}.png")
    return file_url, input_path


async def download_image(response, input_path: str) -> str:
    if response.status == 200:
        content = await response.read()
        orig = Image.open(io.BytesIO(content))
        orig.save(input_path, format='PNG')
        return input_path
    else:
        print('Failed', response.status)


async def handle_download(message, photo=True):
    file_url, input_path = await get_file_data(message, photo)
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            downloaded = await download_image(response, input_path)
    return downloaded
