"""This file contains code to write generated images to disk"""

import base64
import os
import random

from typing import Dict

from constants import GEN_FOLDER


def gen_filename(filetype: str = 'gen', ext: str = 'png') -> str:
    """
    Asynchronously generates a unique filename for storing an image in a specified folder.

    :param filetype: name tag for further recognition by other functions
    :param ext: specify extension
    :return: The absolute path to the generated filename.
    """
    while True:
        filename = os.path.join(GEN_FOLDER, f'{filetype}_{random.randint(100, 999999)}.{ext}')
        if not os.path.exists(filename):
            return os.path.join(os.getcwd(), filename)


def write_image(json_image: Dict) -> str:
    """
    Writes image to a file
    :param json_image: a json file with image in it
    :return: path to a written file
    """
    image = json_image['output']['choices'][0]
    f_name = gen_filename()
    with open(f_name, "wb") as f:
        f.write(base64.b64decode(image["image_base64"]))
    return f_name
