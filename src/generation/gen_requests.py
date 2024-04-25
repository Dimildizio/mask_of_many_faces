"""This file contains code for sending and receiving requests from AI image generation server"""

import random
import requests

from typing import Tuple, Dict, Any

from src.utilities.constants import API, URL, GEN_MODEL, WIDTH, HEIGHT, STEP


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


def send_requests(payload: Dict, headers: Dict) -> Dict:
    """
    Sends and receives request to a distant url to generate image
    :param payload: Info about the image to generate
    :param headers: Info for request including API
    :returns: json with generated image

    """
    response = requests.post(URL, json=payload, headers=headers, stream=True)
    response.raise_for_status()
    return response.json()


def requests_adapter(prompt: str, negative_prompt: str) -> Any:
    """
    Adapter between func call and requesting image
    :param prompt: Prompts what to generate
    :param negative_prompt: what to avoid
    :return: received image
    """
    img_info, api_info = create_request(prompt, negative_prompt)
    img = send_requests(img_info, api_info)
    return img
