from utils import get_yaml


CONFIG = get_yaml()

WIDTH = CONFIG['gen_width']
HEIGHT = CONFIG['gen_height']
STEP = CONFIG['gen_steps']
API = CONFIG['gen_api']
GEN_FOLDER = CONFIG['gen_folder']
URL = CONFIG['gen_url']
GEN_MODEL = CONFIG['gen_model']

FASTAPI_BASE_URL = CONFIG['swapper']

TOKEN = CONFIG['tg_token']
FACE_DIR = CONFIG['face_folder']

SENT_TIME = {}
DELAY_BETWEEN_IMAGES = 2