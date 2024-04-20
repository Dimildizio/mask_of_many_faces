import os
import yaml
from typing import Dict


def get_yaml(filename='config.yaml') -> Dict[str, str]:
    """
    Get info from a YAML file.

    :return: A dictionary containing information.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(dir_path, filename)
    with open(full_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config
