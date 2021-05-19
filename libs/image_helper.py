import os
import re
from typing import Union
from flask import send_from_directory
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def get_path(folder: str = None, basefilename: str = None) -> str:
    filename = find_image_any_format(folder, basefilename)
    if filename:
        return os.path.join(folder, filename)
    else:
        return None


def find_image_any_format(folder: str, basefilename: str) -> Union[str, None]:
    """
    Given a format-less basefilename, try to find the file by appending each of the allowed 
    formats to the given filename and check if the file exists
    :param filename: formatless filename
    :param folder: the relative folder in which to search
    :return: the filename of the image if exists, otherwise None
    """
    for _format in ALLOWED_EXTENSIONS: 
        filename = f"{basefilename}.{_format}"
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            return filename
    return None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_basefilename_safe(basefilename: str) -> bool:
    """
    Check if a filename is secure according to our definition
    - starts with a-z A-Z 0-9 at least one time
    - only contains a-z A-Z 0-9 and _().-
    """
    # allowed_format = "|".join(ALLOWED_EXTENSIONS)
    # # format ALLOWED_EXTENSIONS into regex, eg: ('jpeg','png') --> 'jpeg|png'
    # regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"

    regex = "^[a-zA-Z0-9][a-zA-Z0-9_()-\.]$"
    return re.match(regex, basefilename) is not None


def get_extension(filepath) -> str:
    """
    Return file's extension, for example
    get_extension('image.jpg') returns '.jpg'
    """
    # os.path.split('some/folder/image.jpg')-> ('some/folder', 'image.jpg')
    # os.path.splitext('some/folder/image.jpg')-> ('some/folder/image', '.jpg')
    return os.path.splitext(filepath)[1] 
