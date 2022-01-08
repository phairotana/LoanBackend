import base64
from io import BytesIO
from PIL import Image
import secrets


def base64_pil(base64_str):
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = Image.open(image)
    FIlEPATH = 'storage/images/'
    token_name = secrets.token_hex(10) + '.' + image.format
    path_image = FIlEPATH + token_name
    image.save(path_image)
    return path_image
