import yaml
from typing import Dict


def get_yaml(filename='config.yaml') -> Dict[str, str]:
    """
    Get info from a YAML file.

    :return: A dictionary containing information.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config
