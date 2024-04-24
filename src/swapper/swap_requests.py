import aiohttp
import json
from constants import FASTAPI_BASE_URL


async def send_image_to_swapper(source_path, target_path):
    async with aiohttp.ClientSession() as session:
        data = {"file_path": source_path, 'mode': target_path}
        try:
            async with session.post(f"{FASTAPI_BASE_URL}/swapper", data=data) as response:
                if response.status == 200:
                    return json.loads(await response.text())
                else:
                    return None
        except Exception as e:
            print(f"Failed to send image path to FastAPI: {e}")
            return None
