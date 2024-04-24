"""This file contains logic for handling sending and receiving requests to image generator and save files"""

from typing import Tuple, Dict

from src.generation.gen_write import write_image
from src.generation.gen_requests import requests_adapter


def get_prompts(character: Dict) -> Tuple:
    """

    :param character: a dict with prompt details wht to generate
    :return: tuple of prompt and negative prompt
    """
    beard = f" and {character['hair']} {character['beard']} beard" if character['beard'] else ''
    hair = f" with {character['hair']} hair" if character['hair'] else ''

    prompt = f"One photorealistic D&D game character middle-aged {character['race']} {character['dnd_class']}" \
             f"{hair}{beard}, {character['background']} background, realistic face." \
             f"One person on image, Fantasy art, full body, facial detail, extremely detailed, photorealistic style"
    negative_prompt = f"mutated fingers, fused hands, malformed hands grip, malformed limbs, missing arms, " \
                      f"missing legs, extra arms, extra legs{', tusks, teeth'}"
    return prompt, negative_prompt


async def generate_image(character: Dict) -> str:
    """
    Creates prompts, creates requests, sends requests and saves to file
    :param character: dict with prompt details users choose
    :return: string with a path to generated image
    """
    prompt, negative_prompt = get_prompts(character)
    img_json = requests_adapter(prompt, negative_prompt)
    filename = write_image(img_json)
    return filename
