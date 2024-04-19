import base64
import os
import requests
import random

from typing import Any, Tuple, Dict

from constants import URL, GEN_MODEL, WIDTH, HEIGHT, STEP, API, FOLDER


def generate_image(character: Dict) -> str:
    """
    Creates prompts, creates requests, sends requests and saves to file
    :param character: dict with prompt details users choose
    :return: string with a path to generated image
    """
    prompt, negative_prompt = get_prompts(character)
    img_info, api_info = create_request(prompt, negative_prompt)
    img = send_requests(img_info, api_info)
    filename = write_image(img)
    return filename


def get_prompts(character: Dict) -> Tuple:
    """

    :param character: a dict with prompt details wht to generate
    :return: tuple of prompt and negative prompt
    """
    prompt = f"One photorealistic D&D game character middle-aged {character['race']} {character['dnd_class']}, " \
             f"{character['background']} background. " \
             f"One person on image, Fantasy art, full body, facial detail, extremely detailed, photorealistic style"
    negative_prompt = f"mutated fingers, fused hands, malformed hands grip, malformed limbs, missing arms, " \
                      f"missing legs, extra arms, extra legs{', tusks, teeth'}"
    return prompt, negative_prompt


def create_request(prompt, negative_prompt) -> Tuple:
    """

    Create inputs for the request
    :param prompt: Prompts What to generate
    :param negative_prompt: What to avoid
    :return: Tuple of two dicts with parameters fore request
    """

    payload = {
        "model": GEN_MODEL,
        "prompt": prompt,
        "results": 1,
        "width": WIDTH,
        "height": HEIGHT,
        "steps": STEP,
        "seed": random.randint(0, 9999),
        "negative_prompt": negative_prompt}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {API}"}
    return payload, headers


def send_requests(payload: Dict, headers: Dict) -> Any:
    """
    Sends and receives request to a distant url to generate image
    :param payload: Info about the image to generate
    :param headers: Info for request including API
    :returns: generated image

    """
    response = requests.post(URL, json=payload, headers=headers, stream=True)
    response.raise_for_status()
    return response.json()['outputs']['choices'][0]


def write_image(image: Any) -> str:
    """
    Writes image to a file
    :param image: path to write
    :return: path to a written file
    """
    f_name = gen_filename()
    with open(f_name, "wb") as f:
        f.write(base64.b64decode(image["image_base64"]))
    return f_name


def gen_filename(filetype: str = 'gen', ext: str = 'png'):
    """
    Asynchronously generates a unique filename for storing an image in a specified folder.

    :param filetype: name tag for further recognition by other functions
    :param ext: specify extension
    :return: The absolute path to the generated filename.
    """
    while True:
        filename = os.path.join(FOLDER, f'{filetype}_{random.randint(100, 999999)}.{ext}')
        if not os.path.exists(filename):
            return os.path.join(os.getcwd(), filename)
