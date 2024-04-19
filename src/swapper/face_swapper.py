import cv2
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model
from PIL import Image
from typing import Any, List, Tuple, Optional


app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],  # Allows all origins
                   allow_credentials=True,
                   allow_methods=["*"],  # Allows all methods
                   allow_headers=["*"],)  # Allows all headers

ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATERMARK = '@mask_of_many_faces_bot'


async def get_n_name(name: str, n: int) -> str:
    """
    Generates a new filename by appending a number to the original filename.

    :param name: The original filename.
    :param n: The number (equal to the n-th face of original image faces) to append to the filename.
    :return: A new filename with the number appended before the file extension.
    """
    return f'{name[:-4]}_{n}.png'


def get_swapp() -> FaceAnalysis:
    """
    Initializes, prepares size and returns a FaceAnalysis object for face detection and analysis.

    :return: A FaceAnalysis object configured for use.
    """
    swapp = FaceAnalysis(name='buffalo_l')
    swapp.prepare(ctx_id=0, det_size=(640, 640))
    return swapp


def get_swapper() -> Any:
    """
    Loads and returns a face swapping model.

    :return: A model object for face swapping.
    """
    return get_model('inswapper_128.onnx', download=False)


async def load_face(swapp: FaceAnalysis, img_path: str) -> List:
    """
    Loads a face from an image file using a given FaceAnalysis object.

    :param swapp: A FaceAnalysis object used for detecting faces.
    :param img_path: The path to the image file.
    :return: Detected faces in the image.
    """
    read_img = cv2.imread(img_path)
    faces = swapp.get(read_img)
    return faces


async def filter_multiple_targets(target_faces: List, n: int = 1) -> List:
    """
    Filters and returns the n faces with the largest bbox sizes.

    :param target_faces: List of detected faces.
    :param n: number of faces to filter
    :return: The n the largest faces.
    """
    if len(target_faces) <= n:
        return target_faces
    sorted_faces = sorted(target_faces, key=lambda face: (face.bbox[2] - face.bbox[0]) * (
                                                          face.bbox[3] - face.bbox[1]), reverse=True)
    return sorted_faces[:n]


async def add_watermark_cv(image: Any, watermark_text: str = WATERMARK) -> None:
    """
    Adds a watermark to an image. It has shadow to be seen on white and black.

    :param image: The image to which the watermark will be added. "Any" since it's not worth importing ndarray for that.
    :param watermark_text: The text of the watermark. Defaults to a global variable WATERMARK.
    """
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 1
    color = (255, 255, 255)
    thickness = 1
    text_size = cv2.getTextSize(watermark_text, font, font_scale, thickness)[0]
    padding = 2
    position = (padding, image.shape[0] - padding - text_size[1])
    shadow_position = (position[0] + 1, position[1] + 1)
    cv2.putText(image, watermark_text, shadow_position, font, font_scale, (0, 0, 0), thickness)
    cv2.putText(image, watermark_text, position, font, font_scale, color, thickness)


async def select_target(mode: str) -> Tuple[str, Any]:
    """
    Selects a target image based on the mode (order numbers in json file).

    :param mode: The mode used to select the target image.
    :return: A tuple containing the path to the target image and the image itself in ndarray (Any).
    """
    target_path = mode
    result_img = cv2.imread(mode)
    return target_path, result_img


async def swap_all_target(source_faces: List, result_img: Any, target_faces: List) -> List:
    """
    Swaps faces for a single target from multiple sorts creating different images

    :param source_faces: Detected faces from user images
    :param result_img: A copy of original target image
    :param target_faces: A from the original target image
    :returns: A list of n images (n = len(source_faces))
    """
    result_faces = []
    for face in source_faces:
        new_result_img = result_img.copy()
        for t_face in target_faces:
            new_result_img = SWAPPER.get(new_result_img, t_face, face, paste_back=True)
            break
        await add_watermark_cv(new_result_img)
        result_faces.append(Image.fromarray(cv2.cvtColor(new_result_img, cv2.COLOR_BGR2RGB)))
        #  if len(result_faces) > n:
        #    break
    return result_faces


async def swap_faces(source_path: str, mode: str = '4') -> Optional[List[Image.Image]]:
    """
    Swaps faces between the source image and the target image specified by mode.

    :param source_path: Path to the source image.
    :param mode: Mode specifying the target image or operation.
    :return: A list of PIL Image objects with swapped faces, or None if an error occurs.
    """
    target_path, result_img = await select_target(mode)
    source_faces = await load_face(SWAPP, source_path)
    target_faces = await load_face(SWAPP, target_path)
    target_faces = await filter_multiple_targets(target_faces, n=1)
    try:
        if not target_faces or not source_faces:  # if no faces detected in target face
            raise ValueError('No face detected in targets')
        result_faces = await swap_all_target(source_faces, result_img, target_faces)
    except Exception as e:
        print(f'EXCEPTION {type(e).__name__}: {e}')
        return None
    return result_faces


async def get_face(temp_file: str, mode: str) -> List[str]:
    """
    Processes an image file to swap faces and save the resulting images with a watermark.
    If no faces are detected, it generates an image with a predefined message.

    :param temp_file: The path to the file containing the source image.
    :param mode: The mode specifying what target faces should be swapped with.
    :return: A list of PATHS to the saved image files.
    """
    imgs = await swap_faces(temp_file, mode=mode)
    saved_files = []
    if imgs is None or len(imgs) == 0:
        return
    for i, img in enumerate(imgs):
        name = await get_n_name(temp_file, i)
        root_dir = ROOTDIR+'/temp/result'
        name = os.path.join(root_dir, os.path.basename(name))
        img.save(name, format='PNG')
        saved_files.append(name)
    return saved_files


@app.post('/swapper')
async def extract_face(file_path: str = Form(...), mode: str = Form(...)) -> List[str]:
    """
    FastAPI endpoint to extract faces from an image file and swap them based on the provided mode.
    The modified image(s) are saved and their PATHS are returned.

    :param file_path: The path to the image file to process.
    :param mode: The mode specifying what target faces should be swapped to.
    :return: A list of PATHS to the saved image files.
    """
    saved_faces = await get_face(file_path, mode)
    return saved_faces


# Create instances of detectors and swappers
SWAPP = get_swapp()
SWAPPER = get_swapper()
